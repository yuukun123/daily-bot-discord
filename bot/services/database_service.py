"""
Database Service - Lưu trữ dữ liệu báo cáo hàng ngày
Chỉ lưu dữ liệu vào lúc 7h sáng
"""
import sqlite3
import json
from datetime import datetime
import pytz
from pathlib import Path

class DatabaseService:
    def __init__(self, db_path="data/daily_reports.db"):
        self.db_path = db_path
        
        # Tạo folder data nếu chưa có
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Khởi tạo database
        self.init_database()
    
    def init_database(self):
        """Tạo bảng nếu chưa tồn tại"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS daily_reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                
                -- Thời tiết
                temperature REAL,
                feels_like REAL,
                humidity INTEGER,
                clouds INTEGER,
                visibility REAL,
                weather_description TEXT,
                wind_speed REAL,
                wind_direction TEXT,
                
                -- Giá vàng
                gold_type TEXT,
                gold_buy TEXT,
                gold_sell TEXT,
                
                -- Tỷ giá USD
                usd_black_buy TEXT,
                usd_black_sell TEXT,
                usd_bank_buy TEXT,
                usd_bank_transfer TEXT,
                usd_bank_sell TEXT,
                usd_bank_source TEXT,
                
                -- Thủy triều
                tide_location TEXT,
                tide_high TEXT,
                tide_low TEXT,
                tide_note TEXT,
                
                UNIQUE(date)
            )
        ''')
        
        conn.commit()
        conn.close()
        print("Database initialized successfully")
    
    def save_daily_report(self, weather_data, gold_data, usd_data, tide_data):
        """
        Lưu báo cáo hàng ngày vào database
        CHỈ được gọi vào lúc 7h sáng
        """
        tz = pytz.timezone('Asia/Ho_Chi_Minh')
        now = datetime.now(tz)
        date_str = now.strftime('%Y-%m-%d')
        timestamp_str = now.strftime('%Y-%m-%d %H:%M:%S')
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO daily_reports (
                    date, timestamp,
                    temperature, feels_like, humidity, clouds, visibility, 
                    weather_description, wind_speed, wind_direction,
                    gold_type, gold_buy, gold_sell,
                    usd_black_buy, usd_black_sell, 
                    usd_bank_buy, usd_bank_transfer, usd_bank_sell, usd_bank_source,
                    tide_location, tide_high, tide_low, tide_note
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                date_str, timestamp_str,
                # Weather
                weather_data.get('temperature') if weather_data else None,
                weather_data.get('feels_like') if weather_data else None,
                weather_data.get('humidity') if weather_data else None,
                weather_data.get('clouds') if weather_data else None,
                weather_data.get('visibility') if weather_data else None,
                weather_data.get('description') if weather_data else None,
                weather_data.get('wind_speed') if weather_data else None,
                weather_data.get('wind_direction') if weather_data else None,
                # Gold
                gold_data.get('type') if gold_data else None,
                gold_data.get('buy') if gold_data else None,
                gold_data.get('sell') if gold_data else None,
                # USD
                usd_data['black_market']['buy'] if usd_data else None,
                usd_data['black_market']['sell'] if usd_data else None,
                usd_data['bank']['buy'] if usd_data else None,
                usd_data['bank']['transfer'] if usd_data else None,
                usd_data['bank']['sell'] if usd_data else None,
                usd_data['bank']['source'] if usd_data else None,
                # Tide
                tide_data.get('location') if tide_data else None,
                tide_data.get('high_tide') if tide_data else None,
                tide_data.get('low_tide') if tide_data else None,
                tide_data.get('note') if tide_data else None,
            ))
            
            conn.commit()
            print(f"✅ Đã lưu báo cáo ngày {date_str} vào database")
            return True
            
        except Exception as e:
            print(f"❌ Lỗi khi lưu database: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()
    
    def get_report_by_date(self, date_str):
        """Lấy báo cáo theo ngày (format: YYYY-MM-DD)"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM daily_reports WHERE date = ?', (date_str,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return dict(row)
        return None
    
    def get_latest_reports(self, limit=7):
        """Lấy N báo cáo gần nhất"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM daily_reports ORDER BY date DESC LIMIT ?', (limit,))
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def export_to_json(self, output_file="data/reports_export.json"):
        """Export tất cả data ra JSON"""
        reports = self.get_latest_reports(limit=365)  # 1 năm
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(reports, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Đã export {len(reports)} báo cáo ra {output_file}")
