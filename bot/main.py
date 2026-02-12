import discord
from discord.ext import commands, tasks
import os
import sys
from dotenv import load_dotenv
from datetime import datetime, time as dt_time
import pytz

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import services
from config import Config
from bot.services import WeatherService, GoldService, TideService, USDService
from bot.services.database_service import DatabaseService

# Load environment variables
load_dotenv()

# Validate configuration
Config.validate()

# Cấu hình quyền hạn (Intents)
intents = discord.Intents.default()
intents.message_content = True  # Quan trọng: Phải bật cái này bot mới đọc được tin nhắn

# Tạo đối tượng bot với tiền tố lệnh là "!"
bot = commands.Bot(command_prefix='!', intents=intents)

# Initialize services
weather_service = WeatherService(Config.OPENWEATHER_API_KEY)
gold_service = GoldService(Config.VAPI_KEY)
tide_service = TideService()
usd_service = USDService()
db_service = DatabaseService()  # Database service

# Store channel ID for daily reports
report_channel_id = None


# Sự kiện khi bot đã sẵn sàng hoạt động
@bot.event
async def on_ready():
    print(f'Đã đăng nhập thành công với tên: {bot.user}')
    print(f'Bot ID: {bot.user.id}')
    
    # Load report channel from config if set
    global report_channel_id
    if Config.REPORT_CHANNEL_ID:
        report_channel_id = int(Config.REPORT_CHANNEL_ID)
        print(f'Report channel ID: {report_channel_id}')
    
    # Start all daily report tasks
    if not morning_report_task.is_running():
        morning_report_task.start()
        print('Đã khởi động task báo cáo buổi sáng (07:00)')
    
    if not noon_report_task.is_running():
        noon_report_task.start()
        print('Đã khởi động task báo cáo buổi trưa (12:00)')
    
    if not evening_report_task.is_running():
        evening_report_task.start()
        print('Đã khởi động task báo cáo buổi chiều (18:00)')


async def create_daily_embed():
    """Create a rich embed with all daily information"""
    
    # Fetch all data concurrently
    weather_data = await weather_service.get_weather()
    gold_data = await gold_service.get_gold_price()
    tide_data = await tide_service.get_tide_info()
    usd_data = await usd_service.get_usd_rates()
    
    # Create embed
    embed = discord.Embed(
        title="Báo Cáo Hàng Ngày - TP. Hồ Chí Minh",
        description=f"Cập nhật lúc {datetime.now(pytz.timezone(Config.TIMEZONE)).strftime('%H:%M, %d/%m/%Y')} \n",
        color=discord.Color.blue()
    )
    
    # Add weather information
    if weather_data:
        weather_text = f"""
        **-- Nhiệt độ:** {weather_data['temperature']}°C (cảm giác {weather_data['feels_like']}°C)
        **-- Độ ẩm:** {weather_data['humidity']}%
        **-- Mây:** {weather_data['clouds']}%
        **-- Tầm nhìn:** {weather_data['visibility']} km
        **-- Mô tả:** {weather_data['description'].capitalize()}

        """
        embed.add_field(name="Thời Tiết", value=weather_text, inline=False)
        
        wind_text = f"""
        **-- Tốc độ:** {weather_data['wind_speed']} km/h
        **-- Hướng:** {weather_data['wind_direction']}
        **-----------------------------------------------**
        """
        print("\n\n")
        embed.add_field(name="Gió", value=wind_text, inline=True)
    else:
        embed.add_field(name="Thời tiết", value="⚠️ Không lấy được dữ liệu", inline=False)
    
    # Add gold price information
    if gold_data:
        gold_text = f"""
        **-- Loại:** {gold_data['type']}
        **-- Mua vào:** {gold_data['buy']} VNĐ/lượng
        **-- Bán ra:** {gold_data['sell']} VNĐ/lượng
        **-----------------------------------------------**
        """
        print("\n\n")
        embed.add_field(name="Giá Vàng SJC 9999", value=gold_text, inline=False)
    else:
        embed.add_field(name="Giá Vàng", value="⚠️ Không lấy được dữ liệu", inline=False)
    
    # Add tide information
    if tide_data:
        tide_text = f"""
        **-- Vị trí:** {tide_data['location']}
        **-- Triều lên:** {tide_data['high_tide']}
        **-- Triều xuống:** {tide_data['low_tide']}
        {tide_data['note']}
        **-----------------------------------------------**
        """
        print("\n\n")
        embed.add_field(name="Thủy Triều", value=tide_text, inline=False)
    else:
        embed.add_field(name="Thủy Triều", value="⚠️ Không lấy được dữ liệu", inline=False)
    
    # Add USD exchange rate information
    if usd_data:
        usd_text = f"""
        **Chợ Đen (Tự Do):**
        -- Mua: {usd_data['black_market']['buy']} VNĐ
        -- Bán: {usd_data['black_market']['sell']} VNĐ
        
        **{usd_data['bank']['source']}:**
        -- Mua: {usd_data['bank']['buy']} VNĐ
        -- Chuyển khoản: {usd_data['bank']['transfer']} VNĐ
        -- Bán: {usd_data['bank']['sell']} VNĐ
        **-----------------------------------------------**
        """
        print("\n\n")
        embed.add_field(name="Tỷ Giá USD/VND", value=usd_text, inline=False)
    else:
        embed.add_field(name="Tỷ Giá USD/VND", value="⚠️ Không lấy được dữ liệu", inline=False)
    
    # Set footer
    embed.set_footer(text="Bot by yuu | Dữ liệu từ OpenWeatherMap, vAPI & tygiausd.org")
    
    return embed


# Helper function to send report
async def send_report(time_label):
    """Send report to the configured channel"""
    global report_channel_id
    
    if not report_channel_id:
        print(f"[{time_label}] Chưa set channel cho báo cáo. Dùng !setchannel để set.")
        return
    
    channel = bot.get_channel(report_channel_id)
    if not channel:
        print(f"[{time_label}] Không tìm thấy channel ID: {report_channel_id}")
        return
    
    try:
        embed = await create_daily_embed()
        await channel.send(embed=embed)
        print(f"[{time_label}] Đã gửi báo cáo vào channel: {channel.name}")
    except Exception as e:
        print(f"[{time_label}] Lỗi khi gửi báo cáo: {e}")


# Morning report task (7:00 AM)
@tasks.loop(hours=24)
async def morning_report_task():
    """Send morning report at 7:00 AM and SAVE to database"""
    global report_channel_id
    
    # Fetch all data
    weather_data = await weather_service.get_weather()
    gold_data = await gold_service.get_gold_price()
    tide_data = await tide_service.get_tide_info()
    usd_data = await usd_service.get_usd_rates()
    
    # SAVE TO DATABASE (CHỈ VÀO 7H SÁNG)
    db_service.save_daily_report(weather_data, gold_data, usd_data, tide_data)
    
    # Send report to channel
    await send_report("07:00 Sáng")


@morning_report_task.before_loop
async def before_morning_report():
    """Wait until 7:00 AM before starting"""
    await bot.wait_until_ready()
    await wait_until_time(7, 0, "07:00")


# Noon report task (12:00 PM)
@tasks.loop(hours=24)
async def noon_report_task():
    """Send noon report at 12:00 PM"""
    await send_report("12:00 Trưa")


@noon_report_task.before_loop
async def before_noon_report():
    """Wait until 12:00 PM before starting"""
    await bot.wait_until_ready()
    await wait_until_time(12, 0, "12:00")


# Evening report task (6:00 PM)
@tasks.loop(hours=24)
async def evening_report_task():
    """Send evening report at 6:00 PM"""
    await send_report("18:00 Chiều")


@evening_report_task.before_loop
async def before_evening_report():
    """Wait until 6:00 PM before starting"""
    await bot.wait_until_ready()
    await wait_until_time(18, 0, "18:00")


async def wait_until_time(hour, minute, time_label):
    """Helper function to wait until a specific time"""
    tz = pytz.timezone(Config.TIMEZONE)
    now = datetime.now(tz)
    
    # Calculate next report time
    target_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    
    # If target time has passed today, schedule for tomorrow
    if now >= target_time:
        from datetime import timedelta
        target_time += timedelta(days=1)
    
    # Calculate seconds to wait
    wait_seconds = (target_time - now).total_seconds()
    
    print(f"Báo cáo {time_label} sẽ được gửi lúc {time_label} (còn {wait_seconds/3600:.1f} giờ)")
    
    import asyncio
    await asyncio.sleep(wait_seconds)


# Lệnh: !daily - Gửi báo cáo ngay lập tức
@bot.command()
async def daily(ctx):
    """Gửi báo cáo hàng ngày ngay lập tức"""
    async with ctx.typing():
        embed = await create_daily_embed()
        await ctx.send(embed=embed)


# Lệnh: !setchannel - Set channel cho báo cáo hàng ngày
@bot.command()
async def setchannel(ctx):
    """Set channel hiện tại làm channel nhận báo cáo hàng ngày"""
    global report_channel_id
    report_channel_id = ctx.channel.id
    
    await ctx.send(f"Đã set channel **{ctx.channel.name}** làm channel nhận báo cáo hàng ngày!")
    print(f"Report channel set to: {ctx.channel.name} (ID: {ctx.channel.id})")
    
    # Optionally save to env file for persistence
    # (requires additional implementation)


# Lệnh: !hello - Test command
@bot.command()
async def hello(ctx):
    await ctx.send(f'Xin chào {ctx.author.name}! Tôi là bot thời tiết của bạn. 🌤️')


# Lệnh: !ping - Test command
@bot.command()
async def ping(ctx):
    await ctx.send('Pong! 🏓')


# Chạy bot
if __name__ == "__main__":
    bot.run(Config.DISCORD_TOKEN)