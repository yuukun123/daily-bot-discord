# Database Documentation

## Overview

Bot tự động lưu báo cáo hàng ngày vào SQLite database **chỉ vào 7h sáng**.

**Database location:** `data/daily_reports.db`

---

## Schema

### Table: `daily_reports`

| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER | Primary key (auto increment) |
| `date` | TEXT | Ngày báo cáo (YYYY-MM-DD) |
| **Weather** | | |
| `temperature` | REAL | Nhiệt độ (°C) |
| `feels_like` | REAL | Cảm giác như (°C) |
| `humidity` | INTEGER | Độ ẩm (%) |
| `clouds` | INTEGER | Mây (%) |
| `visibility` | REAL | Tầm nhìn (km) |
| `description` | TEXT | Mô tả thời tiết |
| `wind_speed` | REAL | Tốc độ gió (km/h) |
| `wind_direction` | TEXT | Hướng gió |
| **Gold** | | |
| `gold_type` | TEXT | Loại vàng (SJC 9999) |
| `gold_buy` | TEXT | Giá mua vào |
| `gold_sell` | TEXT | Giá bán ra |
| **USD** | | |
| `usd_bank_buy` | TEXT | Vietcombank mua |
| `usd_bank_transfer` | TEXT | Vietcombank chuyển khoản |
| `usd_bank_sell` | TEXT | Vietcombank bán |
| `usd_black_buy` | TEXT | Chợ đen mua |
| `usd_black_sell` | TEXT | Chợ đen bán |
| **AUD** | | |
| `aud_buy` | TEXT | Vietcombank mua tiền mặt |
| `aud_transfer` | TEXT | Vietcombank chuyển khoản |
| `aud_sell` | TEXT | Vietcombank bán |
| **Tide** | | |
| `tide_location` | TEXT | Vị trí đo |
| `tide_high` | TEXT | Triều lên |
| `tide_low` | TEXT | Triều xuống |
| `tide_note` | TEXT | Ghi chú |
| `created_at` | TIMESTAMP | Thời gian lưu |

---

## Usage

### Query data

```python
import sqlite3

conn = sqlite3.connect('data/daily_reports.db')
cursor = conn.cursor()

# Get latest report
cursor.execute('SELECT * FROM daily_reports ORDER BY date DESC LIMIT 1')
latest = cursor.fetchone()

# Get reports from last 7 days
cursor.execute('SELECT * FROM daily_reports WHERE date >= date("now", "-7 days")')
week_data = cursor.fetchall()

conn.close()
```

### View with SQLite Browser

Download [DB Browser for SQLite](https://sqlitebrowser.org/) and open `data/daily_reports.db`

---

## Notes

- Database chỉ lưu data **1 lần/ngày vào 7h sáng**
- Báo cáo 12h trưa và 6h chiều **không lưu** database
- File database persist locally, không sync cloud (khi deploy cloud cần dùng volumes)
