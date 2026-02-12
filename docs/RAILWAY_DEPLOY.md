# Hướng Dẫn Deploy lên Railway - Chi Tiết Từng Bước

## Bước 1: Chuẩn bị code

### 1.1 Commit tất cả changes lên GitHub

```bash
git add .
git commit -m "Add Railway deployment config"
git push
```

### 1.2 Kiểm tra files cần thiết (đã có sẵn)

- [x] `Procfile` - Chỉ định command chạy bot
- [x] `requirements.txt` - Python dependencies
- [x] `railway.json` - Railway config
- [x] `.env.example` - Template cho env variables

---

## Bước 2: Tạo tài khoản Railway

### 2.1 Đăng ký

1. Vào https://railway.app
2. Click **Start a New Project** hoặc **Login**
3. Đăng nhập bằng **GitHub account** (recommended)
4. Railway sẽ xin quyền truy cập GitHub repos của bạn

### 2.2 Free Tier

Railway free tier cho phép:
- **$5 credit/month** (đủ cho Discord bot chạy 24/7)
- **512 MB RAM**
- **1 GB disk**
- **Unlimited projects**

---

## Bước 3: Deploy Bot

### 3.1 Tạo New Project

1. Trong Railway dashboard, click **New Project**
2. Chọn **Deploy from GitHub repo**
3. Tìm và chọn repo `yuukun123/daily-bot-discord`
4. Railway sẽ tự động:
   - Detect `requirements.txt`
   - Cài đặt Python dependencies
   - Đọc `Procfile` để biết command chạy

### 3.2 Đợi build hoàn thành

Railway sẽ:
1. Clone repo
2. Install dependencies (`pip install -r requirements.txt`)
3. Build project
4. **LƯU Ý:** Bot sẽ CRASH ngay vì chưa có environment variables!

---

## Bước 4: Thiết lập Environment Variables

### 4.1 Vào Settings

1. Click vào project vừa tạo
2. Click tab **Variables** (hoặc Settings → Variables)

### 4.2 Thêm tất cả biến môi trường

Copy từ file `.env` local của bạn:

| Variable Name | Value | Ví dụ |
|---------------|-------|-------|
| `DISCORD_TOKEN` | Bot token từ Discord | `MTQ3MTM0NjYy...` |
| `OPENWEATHER_API_KEY` | API key từ OpenWeather | `56a0f1a575e...` |
| `VAPI_KEY` | API key từ vAPI | `eyJhbGciOiJ...` |
| `REPORT_TIME` | 07:00 | `07:00` |
| `REPORT_CHANNEL_ID` | (để trống) | `` |
| `CITY` | Ho Chi Minh City | `Ho Chi Minh City` |
| `TIMEZONE` | Asia/Ho_Chi_Minh | `Asia/Ho_Chi_Minh` |

**Cách thêm:**
1. Click **New Variable**
2. Nhập `Variable Name` (VD: `DISCORD_TOKEN`)
3. Nhập `Value` (paste API key)
4. Click **Add**
5. Lặp lại cho tất cả variables

### 4.3 Redeploy sau khi thêm variables

Railway sẽ tự động redeploy khi bạn thêm variables.

---

## Bước 5: Kiểm tra Bot đang chạy

### 5.1 Xem Logs

1. Click tab **Deployments**
2. Click deployment mới nhất
3. Xem **Logs** để kiểm tra:

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
3. Bot phải reply: "Xin chào {tên}! Tôi là bot thời tiết của bạn."

### 5.3 Set channel

```
!setchannel
```

Bot sẽ set channel hiện tại làm nơi gửi báo cáo tự động.

---

## Bước 6: Troubleshooting

### Bot bị crash với "ModuleNotFoundError"

**Nguyên nhân:** Thiếu dependency trong `requirements.txt`

**Giải pháp:**
```bash
# Local
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update requirements"
git push
```

Railway sẽ tự động redeploy.

### Bot không reply

**Kiểm tra:**
1. Logs có lỗi không?
2. Discord bot có **Message Content Intent** bật không?
   - Vào Discord Developer Portal
   - Bot → Privileged Gateway Intents
   - Bật **Message Content Intent**

### Database không lưu

**Lưu ý:** Railway restart container thường xuyên → SQLite database bị mất.

**Giải pháp:**
1. Dùng **Railway Volume** để persist database
2. HOẶC dùng external database (PostgreSQL, MongoDB)

**Cách thêm Volume:**
1. Settings → Volumes
2. Click **New Volume**
3. Mount Path: `/app/data`
4. Railway sẽ persist folder `data/`

---

## Bước 7: Theo dõi & Maintain

### 7.1 Monitor usage

1. Railway Dashboard → Project
2. Xem **Metrics**:
   - CPU usage
   - Memory usage
   - Network usage

### 7.2 Xem logs

```
Railway Dashboard → Deployments → View Logs
```

### 7.3 Update code

Mỗi khi push lên GitHub:

```bash
git add .
git commit -m "Update features"
git push
```

Railway tự động:
1. Detect changes
2. Rebuild
3. Redeploy

---

## Bước 8: Tối ưu cho Railway

### 8.1 Reduce memory usage

Trong `bot/main.py`, giảm log verbosity:

```python
# Disable debug logging
logging.basicConfig(level=logging.INFO)
```

### 8.2 Health check (optional)

Thêm endpoint để Railway check bot còn sống:

```python
# Chạy HTTP server đơn giản
from http.server import HTTPServer, BaseHTTPRequestHandler

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'OK')

# Start in background thread
import threading
server = HTTPServer(('0.0.0.0', 8080), HealthHandler)
threading.Thread(target=server.serve_forever, daemon=True).start()
```

---

## Tóm tắt Commands

```bash
# 1. Commit code
git add .
git commit -m "Deploy to Railway"
git push

# 2. Vào Railway dashboard
# - Deploy from GitHub
# - Thêm environment variables
# - Đợi deploy xong

# 3. Test bot
# - Check logs
# - Test !hello trong Discord
# - !setchannel để set channel
```

---

## Chi phí (Free Tier)

- **Monthly credit:** $5
- **Bot usage:** ~$2-3/month (đủ!)
- **Database storage:** Miễn phí (nếu dùng SQLite + Volume)

**Kết luận:** Hoàn toàn FREE cho Discord bot nhỏ! 🎉

---

## Link hữu ích

- Railway Dashboard: https://railway.app/dashboard
- Railway Docs: https://docs.railway.app
- Discord Developer Portal: https://discord.com/developers/applications

---

**Bot của bạn giờ chạy 24/7 trên cloud! Không cần giữ máy tính bật nữa!** 🚀
