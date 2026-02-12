# Hướng Dẫn Deploy lên Render.com - FREE & WORKING

## Tại sao Render?

- ✅ **FREE tier vẫn hoạt động** (Discloud đang quá tải)
- ✅ **512 MB RAM**
- ✅ **Database persist** (với disk storage)
- ✅ **Auto deploy** từ GitHub
- ⚠️ Bot sleep sau 15 phút không hoạt động (auto wake khi có message)

---

## Bước 1: Chuẩn bị - Push code lên GitHub

Render deploy từ GitHub repo, nên cần push code lên:

```bash
# Đảm bảo code đã commit
git add .
git commit -m "Add Render deployment config"
git push
```

**Kiểm tra GitHub:** https://github.com/yuukun123/daily-bot-discord

---

## Bước 2: Tạo tài khoản Render

### 2.1 Đăng ký

1. Vào https://render.com
2. Click **Get Started** hoặc **Sign Up**
3. Chọn **Sign up with GitHub** (nhanh nhất)
4. Authorize Render

### 2.2 Free tier

Render free tier:
- **512 MB RAM**
- **Unlimited builds**
- **Auto sleep** sau 15 phút không dùng
- **Free disk:** 1 GB (cho database)

---

## Bước 3: Deploy Bot

### 3.1 New Web Service

1. Dashboard → **New +** → **Web Service**
2. Connect repository:
   - Click **Connect account** (nếu chưa)
   - Tìm repo `yuukun123/daily-bot-discord`
   - Click **Connect**

### 3.2 Configure service

Render sẽ auto-detect `render.yaml`, nhưng double-check:

| Setting | Value |
|---------|-------|
| **Name** | `daily-weather-bot` |
| **Environment** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `python bot/main.py` |
| **Plan** | `Free` |

### 3.3 Environment Variables

Click **Advanced** → Add environment variables:

| Key | Value | Secret? |
|-----|-------|---------|
| `DISCORD_TOKEN` | (paste token) | ✅ Yes |
| `OPENWEATHER_API_KEY` | (paste key) | ✅ Yes |
| `VAPI_KEY` | (paste key) | ✅ Yes |
| `REPORT_TIME` | `07:00` | No |
| `CITY` | `Ho Chi Minh City` | No |
| `TIMEZONE` | `Asia/Ho_Chi_Minh` | No |
| `REPORT_CHANNEL_ID` | (để trống) | No |

**Lưu ý:** Check "Secret" cho API keys!

### 3.4 Create Web Service

Click **Create Web Service** → Đợi deploy (~3-5 phút)

---

## Bước 4: Kiểm tra Deployment

### 4.1 Xem logs

1. Service dashboard → Tab **Logs**
2. Tìm dòng:
```
Database initialized successfully
Đã đăng nhập thành công với tên: yuu-bot#6567
Đã khởi động task báo cáo buổi sáng (07:00)
```

### 4.2 Test bot

1. Vào Discord server
2. Gõ `!hello`
3. Bot reply (có thể mất 10-15s lần đầu - do wake từ sleep)

### 4.3 Set channel

```
!setchannel
```

---

## Bước 5: Giải quyết Sleep Issue

**Vấn đề:** Bot sleep sau 15 phút không hoạt động.

### Giải pháp 1: Chấp nhận (Free tier)

- Bot auto wake khi có Discord event
- Lần đầu reply sẽ chậm ~10s
- Các lần sau nhanh

### Giải pháp 2: Keep-alive Service (FREE)

Dùng external service ping bot mỗi 14 phút:

**UptimeRobot (FREE):**
1. Vào https://uptimerobot.com
2. Add New Monitor
3. URL: `https://daily-weather-bot.onrender.com` (Render URL)
4. Interval: 5 minutes
5. Bot sẽ không bao giờ sleep!

### Giải pháp 3: Cron Job (trong bot)

Thêm vào `bot/main.py`:

```python
from aiohttp import web

async def health_check(request):
    return web.Response(text="OK")

app = web.Application()
app.router.add_get('/', health_check)

# Run web server
runner = web.AppRunner(app)
await runner.setup()
site = web.TCPSite(runner, '0.0.0.0', 8080)
await site.start()
```

Render sẽ ping port 8080 → Bot không sleep.

---

## Bước 6: Database Persistence

### 6.1 Add Disk Storage

1. Service Settings → **Disks**
2. Add Disk:
   - Name: `data`
   - Mount Path: `/opt/render/project/src/data`
   - Size: 1 GB (free)
3. Save

Database `data/daily_reports.db` sẽ persist!

### 6.2 Verify

Check logs:
```
✅ Đã lưu báo cáo ngày 2026-02-12 vào database
```

---

## Bước 7: Auto Deploy

Mỗi khi push lên GitHub:

```bash
git add .
git commit -m "Update features"
git push
```

Render tự động:
1. Detect changes
2. Rebuild
3. Redeploy

**Disable auto-deploy:** Settings → Build & Deploy → Turn off

---

## Bước 8: Monitor

### 8.1 Metrics

Dashboard → **Metrics**:
- CPU usage
- Memory usage
- Request count

### 8.2 Logs

Tab **Logs** → Real-time output

### 8.3 Shell

Tab **Shell** → SSH into container:
```bash
ls -la data/
python -c "print('test')"
```

---

## Troubleshooting

### Bot không start

**Check logs:**
```
ERROR: Missing DISCORD_TOKEN
```

**Fix:** Add environment variable

### Bot sleep quá nhiều

**Solution:** Dùng UptimeRobot (miễn phí)

### Database bị mất

**Check:** Disk mounted đúng path chưa?
- Mount path: `/opt/render/project/src/data`

### RAM không đủ

Free tier: 512 MB

Bot này dùng ~100-150 MB → Đủ!

---

## So sánh với Discloud

| Feature | Render | Discloud |
|---------|--------|----------|
| **Setup** | GitHub | Upload ZIP |
| **Free tier** | ✅ Working | ❌ Full |
| **RAM** | 512 MB | 100 MB (set) |
| **Database** | ✅ Persist | ✅ Persist |
| **Sleep** | ⚠️ 15 min | ❌ Không |
| **Control** | Web UI | Discord bot |

---

## Commands Tóm Tắt

```bash
# 1. Push code
git add .
git commit -m "Add Render config"
git push

# 2. Vào Render
# - New Web Service
# - Connect GitHub repo
# - Add environment variables
# - Deploy

# 3. Add disk (cho database)
# - Settings → Disks → Add
# - Mount: /opt/render/project/src/data

# 4. (Optional) Setup UptimeRobot
# - Ping Render URL mỗi 5 phút
# - Bot không sleep
```

---

## Links

- **Render Dashboard:** https://dashboard.render.com
- **Docs:** https://render.com/docs
- **Status:** https://status.render.com

---

**Bot của bạn giờ chạy FREE trên Render! Database persist, auto-deploy từ GitHub!** 🚀

**Tip:** Combine với UptimeRobot để bot không bao giờ sleep!
