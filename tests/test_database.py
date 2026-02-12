"""
Test Database Service
"""
import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bot.services.database_service import DatabaseService

# Test data
weather_data = {
    'temperature': 28.5,
    'feels_like': 32.0,
    'humidity': 75,
    'clouds': 40,
    'visibility': 10.0,
    'description': 'Scattered clouds',
    'wind_speed': 15.5,
    'wind_direction': 'Đông Bắc'
}

gold_data = {
    'type': 'SJC Vàng 9999',
    'buy': '178,000',
    'sell': '181,000'
}

usd_data = {
    'black_market': {
        'buy': '26200',
        'sell': '26250'
    },
    'bank': {
        'buy': '25750',
        'transfer': '25780',
        'sell': '26160',
        'source': 'Vietcombank'
    }
}

tide_data = {
    'location': 'TP. Hồ Chí Minh',
    'high_tide': '06:30 (3.2m)',
    'low_tide': '12:45 (0.8m)',
    'note': 'Placeholder data'
}

# Test
db = DatabaseService()

print("Testing save_daily_report...")
db.save_daily_report(weather_data, gold_data, usd_data, tide_data)

print("\nTesting get_latest_reports...")
reports = db.get_latest_reports(5)
for report in reports:
    print(f"Date: {report['date']}, Temp: {report['temperature']}°C, Gold: {report['gold_buy']}")

print("\nTesting export_to_json...")
db.export_to_json()

print("\n✅ All tests passed!")
