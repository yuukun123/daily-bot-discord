# Discord Daily Weather Bot

Một Discord bot tự động gửi báo cáo hàng ngày về thời tiết, giá vàng, tỷ giá USD, tỷ giá AUD và thủy triều cho TP. Hồ Chí Minh.

## Tính năng

- Báo cáo thời tiết hàng ngày (nhiệt độ, độ ẩm, gió, mây, tầm nhìn)
- Giá vàng SJC 9999 (mua/bán)
- Tỷ giá USD/VND (ngân hàng Vietcombank + chợ đen)
- Tỷ giá AUD/VND (Vietcombank)
- Thông tin thủy triều (triều lên/xuống)
- Tự động gửi báo cáo vào 3 thời điểm: 7h sáng, 12h trưa, 6h chiều
- Lưu lịch sử báo cáo vào database SQLite (chỉ 7h sáng)
- Lệnh thủ công: !daily, !hello, !ping, !setchannel

## Nguồn dữ liệu

- **Thời tiết:** [OpenWeatherMap API](https://openweathermap.org/)
- **Giá vàng:** [vAPI - Vietnam Gold Price API](https://vapi.vn/)
- **Tỷ giá USD:** [tygiausd.org](https://tygiausd.org/) (scraping)
- **Tỷ giá AUD:** [Vietcombank XML API](https://portal.vietcombank.com.vn/)
- **Thủy triều:** Hardcoded data (Vũng Tàu)

## Cài đặt nhanh

### 1. Clone repository

```bash
git clone https://github.com/your-username/daily-bot-discord.git
cd daily-bot-discord
```

### 2. Cài đặt dependencies

```bash
pip install -r requirements.txt
```

### 3. Thiết lập môi trường

Copy file `.env.example` thành `.env` và điền API keys:

```bash
cp .env.example .env
```

Chỉnh sửa `.env`:
```env
DISCORD_TOKEN='your_discord_bot_token'
OPENWEATHER_API_KEY='your_openweather_key'
VAPI_KEY='your_vapi_key'
```

### 4. Chạy bot

**Windows:**
```bash
scripts\start_bot.bat
```

**Linux/Mac:**
```bash
python bot/main.py
```

## Commands

| Command | Mô tả |
|---------|-------|
| `!daily` | Gửi báo cáo ngay lập tức |
| `!setchannel` | Set channel nhận báo cáo tự động |
| `!hello` | Test bot |
| `!ping` | Check latency |

## Cấu trúc project

```
daily-bot-discord/
├── bot/                    # Main bot code
│   ├── main.py            # Bot entry point
│   └── services/          # Service modules
│       ├── weather_service.py
│       ├── gold_service.py
│       ├── tide_service.py
│       └── usd_service.py
├── tests/                 # Test files
├── scripts/               # Utility scripts
│   └── start_bot.bat     # Windows launcher
├── docs/                  # Documentation
├── config.py              # Configuration
├── .env                   # Environment variables (git ignored)
├── .env.example           # Example env template
└── requirements.txt       # Python dependencies
```

## Lấy API Keys

### Discord Bot Token
1. Vào [Discord Developer Portal](https://discord.com/developers/applications)
2. Tạo New Application
3. Vào tab **Bot** → Reset Token
4. Copy token vào `.env`

### OpenWeatherMap API
1. Đăng ký tại [OpenWeatherMap](https://openweathermap.org/api)
2. Tạo API key (free tier)
3. Copy vào `.env`

### vAPI Key
1. Đăng ký tại [vAPI](https://vapi.vnappmob.com/)
2. Request API key
3. Copy vào `.env`

## Chạy Bot

### Local Windows

**Cách 1: Chạy thủ công**

Double-click file:
```
scripts\start_bot.bat
```

**Cách 2: Auto-start khi Windows boot**

1. `Win + R` → gõ `taskschd.msc` → Enter
2. Create Basic Task
3. Name: `Discord Weather Bot`
4. Trigger: **When I log on**
5. Action: **Start a program**
6. Program: `D:\DATA\Code\daily-bot-discord\scripts\start_bot.bat`
7. Finish

Bot sẽ tự động chạy mỗi khi bật máy!

**Xem chi tiết:** [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)

## Development

```bash
# Install dev dependencies
pip install -r requirements.txt

# Run tests
python -m pytest tests/

# Format code
black bot/
```

## License

MIT License - xem file [LICENSE](LICENSE)

## Contributing

Pull requests are welcome! For major changes, please open an issue first.

## Support

Có vấn đề? Tạo issue trên [GitHub Issues](https://github.com/your-username/daily-bot-discord/issues)

---

Made with love by yuu