# Hướng Dẫn Deploy lên Discloud Bot

## Giới thiệu Discloud

Discloud là platform hosting chuyên cho Discord bots với:
- **Free tier:** Miễn phí
- **512 MB RAM:** Đủ cho Discord bot
- **Auto restart:** Bot tự động khởi động lại
- **Backup:** Tự động backup mỗi 24h
- **Database persist:** SQLite được lưu trữ

---

## Bước 1: Chuẩn bị

### 1.1 File cấu hình Discloud

File `discloud.config` đã được tạo sẵn:

```json
{
  "NAME": "Daily Weather Bot",
  "AVATAR": "https://i.imgur.com/placeholder.png",
  "TYPE": "bot",
  "MAIN": "bot/main.py",
  "RAM": "512",
  "AUTORESTART": true,
  "VERSION": "recommended",
  "APT": "tools"
}
```

### 1.2 Tạo file .zip

**Windows PowerShell:**
```powershell
cd D:\DATA\Code\daily-bot-discord
Compress-Archive -Path bot,config.py,requirements.txt,discloud.config,.env -DestinationPath discloud-deploy.zip -Force
```

**LƯU Ý:** 
- Discloud CHO PHÉP upload file `.env` trực tiếp trong ZIP!
- Không cần set environment variables manual

---

## Bước 2: Tạo tài khoản Discloud

### 2.1 Đăng ký

1. Vào https://discloudbot.com
2. Click **Login** (góc trên)
3. Login bằng **Discord** (nhanh nhất)
4. Authorize Discloud Bot

### 2.2 Verify

Discord bot sẽ gửi message verify → Click button để confirm.

---

## Bước 3: Upload Bot

### 3.1 Dùng Discord Commands

Discloud hoạt động hoàn toàn qua **Discord bot commands**!

1. Mở Discord
2. Tìm **Discloud Bot** trong server hoặc DM
3. Gõ lệnh:

```
/upload
```

### 3.2 Upload file ZIP

1. Bot sẽ yêu cầu: "Please send the ZIP file"
2. Drag & drop `discloud-deploy.zip` vào chat
3. Gửi file
4. Discloud sẽ:
   - Extract ZIP
   - Đọc `discloud.config`
   - Đọc `.env` từ ZIP
   - Install dependencies
   - Start bot

### 3.3 Đợi deployment

Bot Discloud sẽ reply:
```
✅ Application uploaded successfully!
⏳ Starting application...
✅ Application started!
```

---

## Bước 4: Quản lý Bot

### 4.1 Commands chính

Tất cả commands đều dùng qua Discord:

| Command | Mô tả |
|---------|-------|
| `/status` | Xem trạng thái bot |
| `/logs` | Xem logs (100 dòng gần nhất) |
| `/restart` | Restart bot |
| `/stop` | Dừng bot |
| `/start` | Khởi động bot |
| `/backup` | Tạo backup ngay |
| `/ram` | Xem RAM usage |

### 4.2 Xem logs

```
/logs
```

Discloud bot sẽ gửi file `logs.txt` chứa output của bot.

---

## Bước 5: Kiểm tra Bot

### 5.1 Check status

```
/status
```

Response:
```
🟢 Status: Online
💾 RAM: 145/512 MB
🔄 Uptime: 2h 15m
```

### 5.2 Test trong Discord server

1. Vào Discord server có bot
2. Gõ `!hello`
3. Bot reply: "Xin chào! Tôi là bot thời tiết của bạn."

### 5.3 Set channel

```
!setchannel
```

---

## Bước 6: Update Bot

Khi cần update code:

### 6.1 Tạo ZIP mới

```powershell
# Sửa code local
cd D:\DATA\Code\daily-bot-discord
Compress-Archive -Path bot,config.py,requirements.txt,discloud.config,.env -DestinationPath discloud-deploy.zip -Force
```

### 6.2 Upload lại

```
/upload
```

Gửi file ZIP mới → Discloud tự động update!

---

## Bước 7: Environment Variables

### Cách 1: Include trong ZIP (Recommended)

File `.env` được đọc tự động từ ZIP:

```env
DISCORD_TOKEN=...
OPENWEATHER_API_KEY=...
VAPI_KEY=...
REPORT_TIME=07:00
CITY=Ho Chi Minh City
TIMEZONE=Asia/Ho_Chi_Minh
```

**Upload ZIP với .env bên trong → Xong!**

### Cách 2: Set qua commands (alternative)

```
/config set DISCORD_TOKEN "your_token"
/config set OPENWEATHER_API_KEY "your_key"
```

---

## Bước 8: Database

### 8.1 SQLite Persistence

Discloud **PERSIST** database! 

File `data/daily_reports.db` sẽ:
- ✅ Được lưu khi restart
- ✅ Backup mỗi 24h
- ✅ Không bị mất

### 8.2 Tạo folder data

Discloud tự động tạo folder `data/` khi bot chạy.

---

## Troubleshooting

### Bot không start

**Check logs:**
```
/logs
```

**Common issues:**
- Missing Discord token
- Wrong Python version
- Missing dependencies

### Update không có hiệu lực

```
/restart
```

### RAM không đủ

Free tier: 512 MB

Nếu cần thêm → Upgrade plan

---

## So sánh Platforms

| Feature | Discloud | Square Cloud |
|---------|----------|--------------|
| **Setup** | Discord commands | Web upload |
| **Free RAM** | 512 MB | 256 MB |
| **Database** | ✅ Persist | ❌ Không persist |
| **Env vars** | Include in ZIP | Manual set |
| **Logs** | Discord command | Web dashboard |
| **Backup** | Auto 24h | Không có |
| **Control** | Discord bot | Web UI |

**Discloud = Tốt hơn cho Discord bots!**

---

## Commands Tóm Tắt

```powershell
# 1. Tạo ZIP (bao gồm .env!)
cd D:\DATA\Code\daily-bot-discord
Compress-Archive -Path bot,config.py,requirements.txt,discloud.config,.env -DestinationPath discloud-deploy.zip -Force

# 2. Discord
/upload
# Gửi file discloud-deploy.zip

# 3. Kiểm tra
/status
/logs

# 4. Test
# Discord server: !hello
```

---

## Chi phí

**Free Tier:**
- **RAM:** 512 MB
- **Storage:** 1 GB
- **Backup:** 24h auto
- **Uptime:** 24/7

**100% miễn phí!**

---

## Links

- **Website:** https://discloudbot.com
- **Docs:** https://docs.discloudbot.com
- **Discord:** https://discord.gg/discloud
- **Dashboard:** https://dash.discloudbot.com

---

**Bot của bạn giờ chạy 24/7 trên Discloud với database persistence!** 🚀

**Ưu điểm Discloud:**
- ✅ Control hoàn toàn qua Discord
- ✅ Database được persist
- ✅ Auto backup
- ✅ 512 MB RAM (nhiều hơn Square Cloud)
- ✅ .env trong ZIP (không cần set manual)
