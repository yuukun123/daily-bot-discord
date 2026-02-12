# 🤖 Discord Daily Weather Bot

Một Discord bot tự động gửi báo cáo hàng ngày về thời tiết, giá vàng, tỷ giá USD và thủy triều cho TP. Hồ Chí Minh.

## ✨ Tính năng

- 📅 **3 báo cáo tự động mỗi ngày** (07:00, 12:00, 18:00)
- 🌤️ **Thời tiết & gió** từ OpenWeatherMap
- 💰 **Giá vàng SJC miếng 1L** từ vAPI (multi-source fallback)
- 💵 **Tỷ giá USD/VND** từ tygiausd.org (chợ đen + ngân hàng)
- 🌊 **Thông tin thủy triều**
- 🎨 **Rich Discord embed** với icons đẹp mắt

## 🚀 Cài đặt nhanh

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

## 📋 Commands

| Command | Mô tả |
|---------|-------|
| `!daily` | Gửi báo cáo ngay lập tức |
| `!setchannel` | Set channel nhận báo cáo tự động |
| `!hello` | Test bot |
| `!ping` | Check latency |

## 🏗️ Cấu trúc project

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

## 🔑 Lấy API Keys

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

## 📡 Deploy

Xem hướng dẫn chi tiết trong [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)

**Tóm tắt:**
- ✅ **Local:** Chạy `start_bot.bat` hoặc dùng Task Scheduler
- ✅ **Cloud:** Railway, Render, PythonAnywhere

## 🛠️ Development

```bash
# Install dev dependencies
pip install -r requirements.txt

# Run tests
python -m pytest tests/

# Format code
black bot/
```

## 📝 License

MIT License - xem file [LICENSE](LICENSE)

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first.

## 📞 Support

Có vấn đề? Tạo issue trên [GitHub Issues](https://github.com/your-username/daily-bot-discord/issues)

---

Made with ❤️ by yuu