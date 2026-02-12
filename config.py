"""
Configuration management for the bot
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Discord
    DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
    
    # API Keys
    OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')
    VAPI_KEY = os.getenv('VAPI_KEY')
    
    # Bot Settings
    REPORT_TIME = os.getenv('REPORT_TIME', '07:00')  # Default 7:00 AM
    REPORT_CHANNEL_ID = os.getenv('REPORT_CHANNEL_ID', '1471349583518109891')
    
    # Location
    CITY = "Ho Chi Minh City"
    COUNTRY_CODE = "VN"
    TIMEZONE = "Asia/Ho_Chi_Minh"
    
    @classmethod
    def validate(cls):
        """Validate that all required config is set"""
        required = {
            'DISCORD_TOKEN': cls.DISCORD_TOKEN,
            'OPENWEATHER_API_KEY': cls.OPENWEATHER_API_KEY,
            'VAPI_KEY': cls.VAPI_KEY,
        }
        
        missing = [key for key, value in required.items() if not value]
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")
        
        return True
