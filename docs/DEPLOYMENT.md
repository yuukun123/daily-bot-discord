# Local Deployment Guide

## Chạy Bot trên Windows

### Cách 1: Chạy thủ công

Double-click:
```
scripts\start_bot.bat
```

### Cách 2: Auto-start (Task Scheduler)

1. `Win + R` → `taskschd.msc`
2. Create Basic Task → Name: `Discord Weather Bot`
3. Trigger: **When I log on**
4. Action: Start program: `D:\DATA\Code\daily-bot-discord\scripts\start_bot.bat`
5. Finish

Bot tự động chạy mỗi khi bật máy!

## Commands

```
!hello          - Test bot
!setchannel     - Set channel báo cáo
!daily          - Gửi báo cáo ngay
!ping           - Check latency
```

## Database

Bot tự động lưu dữ liệu 7h sáng vào:
```
data/daily_reports.db
```

## Troubleshooting

**Bot không start:** Check `.env` có đủ API keys

**Bot crash:** Restart `scripts\start_bot.bat`

**Tắt bot:** Đóng cửa sổ CMD hoặc Task Manager → End python.exe

---

**Chi tiết:** Xem deployment_guide artifact
