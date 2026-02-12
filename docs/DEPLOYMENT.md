# Hướng Dẫn Chạy Bot 24/7 trên Windows

## 🎯 Giải pháp 1: Chạy trong Terminal riêng (Nhanh nhất)

**Cách 1a: Dùng file batch đã tạo sẵn**

1. Double-click file [start_bot.bat](file:///d:/DATA/Code/daily-weather-bot/start_bot.bat)
2. Một cửa sổ Command Prompt sẽ mở ra và bot chạy
3. **Giữ cửa sổ này mở** - đừng tắt
4. Bạn có thể đóng IDE, minimize cửa sổ xuống taskbar

> [!TIP]
> Cửa sổ này phải mở suốt để bot hoạt động. Khi khởi động lại máy, chỉ cần double-click `start_bot.bat` lại.

**Cách 1b: Chạy manual**

1. Mở PowerShell/CMD
2. Chạy lệnh:
```powershell
cd D:\DATA\Code\daily-weather-bot
conda activate myENV
python src/main.py
```
3. Giữ cửa sổ PowerShell mở

---

## ⚙️ Giải pháp 2: Windows Task Scheduler (Tự động khởi động)

Bot sẽ tự động chạy khi bật máy.

### Bước 1: Tạo scheduled task

1. Nhấn `Win + R`, gõ `taskschd.msc`, Enter
2. Click **Create Basic Task** (bên phải)
3. **Name:** `Discord Weather Bot`
4. **Trigger:** Chọn **When I log on** (khi đăng nhập)
5. **Action:** Chọn **Start a program**
6. **Program/script:** 
   ```
   D:\DATA\Code\daily-weather-bot\start_bot.bat
   ```
7. **Start in:** 
   ```
   D:\DATA\Code\daily-weather-bot
   ```
8. Finish

### Bước 2: Test ngay

1. Trong Task Scheduler, tìm task **Discord Weather Bot**
2. Right-click → **Run**
3. Bot sẽ khởi động trong cửa sổ CMD

> [!IMPORTANT]
> Task Scheduler sẽ tự chạy bot mỗi khi bạn đăng nhập Windows!

---

## ☁️ Giải pháp 3: Deploy lên Cloud (Chạy 24/7 thực sự)

Nếu bạn muốn bot chạy liên tục ngay cả khi tắt máy:

### Option A: Railway (Free tier - Recommended)

1. Tạo file `requirements.txt` (đã có sẵn)
2. Tạo file `Procfile`:
   ```
   worker: python src/main.py
   ```
3. Push code lên GitHub
4. Đăng ký [Railway.app](https://railway.app)
5. Connect GitHub repo
6. Add environment variables (.env)
7. Deploy!

### Option B: Render (Free tier)

Tương tự Railway, dùng Render.com

### Option C: PythonAnywhere (Free tier có hạn chế)

- 1 web app miễn phí
- Phù hợp cho testing

---

## 🔧 Giải pháp 4: Chạy ẩn (Background - Không hiện cửa sổ)

Tạo file VBScript để chạy bot ẩn:

**File: `start_bot_hidden.vbs`**
```vbscript
Set WshShell = CreateObject("WScript.Shell")
WshShell.Run chr(34) & "D:\DATA\Code\daily-weather-bot\start_bot.bat" & chr(34), 0
Set WshShell = Nothing
```

Double-click file `.vbs` → Bot chạy ngầm (không hiện cửa sổ)

> [!WARNING]
> Khó debug vì không thấy output. Chỉ dùng khi bot đã chạy ổn định.

---

## 📊 So sánh các phương pháp

| Phương pháp | Ưu điểm | Nhược điểm | Phù hợp cho |
|-------------|---------|------------|-------------|
| **Terminal riêng** | Đơn giản, dễ debug | Phải giữ cửa sổ mở | Development/Testing |
| **Task Scheduler** | Tự động khi boot | Vẫn cần máy bật | PC chạy 24/7 |
| **Cloud (Railway)** | Chạy 24/7 thật sự | Cần setup thêm | Production |
| **VBS Hidden** | Không thấy cửa sổ | Khó debug | Production local |

## 🎯 Khuyến nghị

- **Đang dev:** Dùng Giải pháp 1 (terminal riêng)
- **PC bật suốt:** Dùng Giải pháp 2 (Task Scheduler)
- **Muốn 24/7:** Dùng Giải pháp 3 (Railway/Render)

---

## ✅ Kiểm tra bot đang chạy

**Windows:**
```powershell
Get-Process python | Where-Object {$_.CommandLine -like "*main.py*"}
```

**Hoặc:** Mở Task Manager → tìm process `python.exe`

---

## 🛑 Dừng bot

- **Terminal:** Nhấn `Ctrl + C`
- **Task Manager:** End task `python.exe`
- **Task Scheduler:** Right-click task → End
