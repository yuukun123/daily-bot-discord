# Database Feature - Lưu trữ báo cáo hàng ngày

## Tính năng

Bot tự động lưu dữ liệu vào SQLite database **chỉ vào lúc 7h sáng mỗi ngày**.

## Database Schema

**Table: daily_reports**

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| date | TEXT | Ngày (YYYY-MM-DD) |
| timestamp | TEXT | Thời gian đầy đủ |
| **Thời tiết** | | |
| temperature | REAL | Nhiệt độ (°C) |
| feels_like | REAL | Cảm giác như (°C) |
| humidity | INTEGER | Độ ẩm (%) |
| clouds | INTEGER | Mây (%) |
| visibility | REAL | Tầm nhìn (km) |
| weather_description | TEXT | Mô tả thời tiết |
| wind_speed | REAL | Tốc độ gió (km/h) |
| wind_direction | TEXT | Hướng gió |
| **Giá vàng** | | |
| gold_type | TEXT | Loại vàng |
| gold_buy | TEXT | Giá mua vào |
| gold_sell | TEXT | Giá bán ra |
| **Tỷ giá USD** | | |
| usd_black_buy | TEXT | Chợ đen - Mua |
| usd_black_sell | TEXT | Chợ đen - Bán |
| usd_bank_buy | TEXT | Ngân hàng - Mua |
| usd_bank_transfer | TEXT | Ngân hàng - CK |
| usd_bank_sell | TEXT | Ngân hàng - Bán |
| usd_bank_source | TEXT | Tên ngân hàng |
| **Thủy triều** | | |
| tide_location | TEXT | Vị trí |
| tide_high | TEXT | Triều lên |
| tide_low | TEXT | Triều xuống |
| tide_note | TEXT | Ghi chú |

## Usage

### 1. Tự động lưu (7h sáng)

Bot tự động lưu mỗi sáng lúc 7h - không cần làm gì cả!

### 2. Query database bằng Python

```python
from bot.services.database_service import DatabaseService

db = DatabaseService()

# Lấy báo cáo hôm nay
report = db.get_report_by_date('2026-02-12')
print(f"Nhiệt độ: {report['temperature']}°C")

# Lấy 7 ngày gần nhất
reports = db.get_latest_reports(7)
for r in reports:
    print(f"{r['date']}: {r['temperature']}°C, Gold: {r['gold_buy']}")

# Export ra JSON
db.export_to_json("my_export.json")
```

### 3. File locations

- **Database:** `data/daily_reports.db` (SQLite)
- **Exports:** `data/reports_export.json`
- **Folder `data/` trong `.gitignore`** - không commit lên Git

## Test

```bash
python tests/test_database.py
```

## Tại sao chỉ lưu 7h sáng?

- **Đúng với mục đích:** Data buổi sáng là quan trọng nhất (đầu ngày)
- **Tránh duplicate:** Không lưu trùng lặp 3 lần/ngày
- **Tiết kiệm:** Database nhỏ gọn, dễ quản lý
- **Consistent:** Mỗi ngày 1 record duy nhất

## Bonus Commands (có thể thêm sau)

Thêm commands để query database:

```python
@bot.command()
async def history(ctx, days: int = 7):
    """Xem lịch sử N ngày gần nhất"""
    reports = db.get_latest_reports(days)
    # Format và gửi
```

---

**Database tự động hoạt động! Không cần config gì thêm.** 
