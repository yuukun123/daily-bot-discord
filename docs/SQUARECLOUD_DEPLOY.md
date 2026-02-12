# Hướng Dẫn Deploy lên Square Cloud

## Giới thiệu Square Cloud

Square Cloud là platform hosting chuyên cho Discord bots với:
- **Free tier:** Miễn phí hoàn toàn
- **Easy setup:** Deploy trong vài phút
- **Auto restart:** Bot tự động khởi động lại khi crash
- **Dashboard:** Quản lý dễ dàng

---

## Bước 1: Chuẩn bị code

### 1.1 Tạo file cấu hình Square Cloud

File `squarecloud.app` đã được tạo sẵn với nội dung:

```ini
MAIN=bot/main.py
DISPLAY_NAME=Daily Weather Bot
DESCRIPTION=Discord bot gửi báo cáo thời tiết, giá vàng, USD 3 lần/ngày
VERSION=recommended
SUBDOMAIN=daily-weather-bot
```

### 1.2 Tạo file .zip để upload

**Windows PowerShell:**
```powershell
# Đảm bảo đang ở folder project
cd D:\DATA\Code\daily-bot-discord

# Tạo file zip (không bao gồm .git, .env, data/)
Compress-Archive -Path bot,config.py,requirements.txt,squarecloud.app,.env.example -DestinationPath daily-bot-discord.zip -Force
```

**HOẶC dùng GUI:**
1. Chọn các files/folders: `bot/`, `config.py`, `requirements.txt`, `squarecloud.app`, `.env.example`
2. Right-click → Send to → Compressed (zipped) folder
3. Đặt tên: `daily-bot-discord.zip`

**LƯU Ý:** KHÔNG zip toàn bộ folder! Chỉ zip các files cần thiết.

---

## Bước 2: Tạo tài khoản Square Cloud

### 2.1 Đăng ký

1. Vào https://squarecloud.app
2. Click **Sign Up** (góc trên bên phải)
3. Chọn phương thức đăng ký:
   - **Discord** (Recommended - nhanh nhất)
   - Email
   - GitHub

### 2.2 Verify email (nếu dùng email)

Kiểm tra inbox và click link verify.

---

## Bước 3: Upload Bot

### 3.1 Vào Dashboard

1. Login vào Square Cloud
2. Click **Dashboard**
3. Click **Upload Application**

### 3.2 Upload file .zip

1. Click **Choose File**
2. Chọn `daily-bot-discord.zip` vừa tạo
3. Click **Upload**

Square Cloud sẽ:
- Extract zip file
- Detect `squarecloud.app` config
- Read `requirements.txt`
- Install Python dependencies
- Start bot

### 3.3 Đợi deployment

Màn hình sẽ hiển thị:
```
Installing dependencies...
✓ discord.py==2.3.2
✓ aiohttp==3.9.1
✓ python-dotenv==1.0.0
...
Starting application...
```

---

## Bước 4: Thiết lập Environment Variables

Bot sẽ crash ngay vì thiếu environment variables!

### 4.1 Vào Settings

1. Trong Dashboard, click vào bot vừa upload
2. Click tab **Settings** hoặc **Config**
3. Tìm phần **Environment Variables**

### 4.2 Thêm variables

Click **Add Variable** và thêm từng cái:

| Name | Value |
|------|-------|
| `DISCORD_TOKEN` | Bot token từ Discord Developer Portal |
| `OPENWEATHER_API_KEY` | API key từ OpenWeatherMap |
| `VAPI_KEY` | API key từ vAPI |
| `REPORT_TIME` | `07:00` |
| `REPORT_CHANNEL_ID` | (để trống) |
| `CITY` | `Ho Chi Minh City` |
| `TIMEZONE` | `Asia/Ho_Chi_Minh` |

**Cách thêm từng variable:**
1. Name: `DISCORD_TOKEN`
2. Value: Paste token
3. Click **Add**
4. Lặp lại cho tất cả variables

### 4.3 Restart bot

Sau khi thêm xong variables:
1. Click **Restart** hoặc **Reboot**
2. Bot sẽ khởi động lại với env vars mới

---

## Bước 5: Kiểm tra Bot

### 5.1 Xem Console Logs

1. Trong Dashboard, click tab **Console** hoặc **Logs**
2. Xem output:

```
Database initialized successfully
Đã đăng nhập thành công với tên: yuu-bot#6567
Bot ID: 1471346625229230183
Đã khởi động task báo cáo buổi sáng (07:00)
Đã khởi động task báo cáo buổi trưa (12:00)
Đã khởi động task báo cáo buổi chiều (18:00)
```

### 5.2 Test trong Discord

1. Vào Discord server
2. Gõ `!hello`
3. Bot reply: "Xin chào! Tôi là bot thời tiết của bạn."

### 5.3 Set channel

```
!setchannel
```

Bot sẽ set channel hiện tại để gửi báo cáo tự động.

---

## Bước 6: Database Storage

### 6.1 Vấn đề với SQLite

Square Cloud **không persist files** khi restart → Database SQLite sẽ bị mất!

### 6.2 Giải pháp

**Option 1: Chấp nhận (Recommended cho start)**
- Database chỉ để track lịch sử
- Không critical → OK nếu mất

**Option 2: Dùng External Database**
- MongoDB Atlas (free tier)
- PostgreSQL (free tier từ ElephantSQL)
- JSON file trên cloud storage

**Option 3: Disable database**

Nếu không cần database, comment out trong `bot/main.py`:

```python
# db_service = DatabaseService()  # Disable database
```

```python
# db_service.save_daily_report(...)  # Comment out save
```

---

## Bước 7: Monitor & Manage

### 7.1 Dashboard features

- **Console:** Xem logs real-time
- **Status:** CPU, RAM usage
- **Settings:** Config bot
- **Restart:** Khởi động lại bot

### 7.2 Auto-restart

Square Cloud tự động restart bot khi:
- Crash
- Out of memory
- Error

### 7.3 Update bot

Khi cần update code:

1. Sửa code local
2. Tạo file .zip mới:
   ```powershell
   Compress-Archive -Path bot,config.py,requirements.txt,squarecloud.app -DestinationPath daily-bot-discord-v2.zip -Force
   ```
3. Dashboard → **Upload New Version**
4. Chọn file zip mới
5. Bot tự động restart với code mới

---

## Bước 8: Troubleshooting

### Bot không start

**Kiểm tra:**
1. Console logs có lỗi gì?
2. Environment variables đã đủ chưa?
3. `squarecloud.app` có đúng path `MAIN=bot/main.py`?

### Bot crash liên tục

**Nguyên nhân phổ biến:**
- Missing environment variable
- Wrong Discord token
- API key hết hạn

**Fix:** Check Console logs để xem error message

### Database errors

Nếu thấy lỗi database:
```python
# Disable database trong main.py
# db_service = DatabaseService()
```

---

## Chi phí

**Free Tier:**
- **RAM:** 256 MB (đủ cho Discord bot)
- **Storage:** 512 MB
- **Uptime:** 24/7
- **Apps:** Unlimited

**Hoàn toàn miễn phí cho bot này!**

---

## So sánh Railway vs Square Cloud

| Feature | Railway | Square Cloud |
|---------|---------|--------------|
| **Setup** | GitHub/CLI | Upload ZIP |
| **Free RAM** | 512 MB | 256 MB |
| **Database** | Persist (with Volume) | Không persist |
| **Auto Deploy** | Git push | Manual upload |
| **Logs** | Tốt | Tốt |
| **Restart** | Auto | Auto |

**Recommendation:**
- **Square Cloud:** Đơn giản, không cần GitHub, dễ dùng
- **Railway:** Professional hơn, auto deploy, persist data

---

## Commands Tóm Tắt

```powershell
# 1. Tạo ZIP file
cd D:\DATA\Code\daily-bot-discord
Compress-Archive -Path bot,config.py,requirements.txt,squarecloud.app -DestinationPath daily-bot-discord.zip -Force

# 2. Vào Square Cloud
# - Upload ZIP
# - Thêm Environment Variables
# - Restart bot

# 3. Test
# Discord: !hello
# Discord: !setchannel
```

---

## Links

- **Square Cloud:** https://squarecloud.app
- **Dashboard:** https://squarecloud.app/dashboard
- **Documentation:** https://docs.squarecloud.app
- **Discord Support:** https://discord.gg/squarecloud

---

**Bot của bạn giờ chạy 24/7 trên Square Cloud!** 🚀

**Tip:** Dùng Square Cloud cho testing, Railway cho production!
