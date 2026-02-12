"""
Weather service to fetch weather data from OpenWeatherMap API
"""
import aiohttp
import os
from datetime import datetime

class WeatherService:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"
        
    async def get_weather(self, city="Ho Chi Minh City", country_code="VN"):
        """
        Fetch current weather data for Ho Chi Minh City
        Returns: dict with weather information or None if error
        """
        params = {
            "q": f"{city},{country_code}",
            "appid": self.api_key,
            "units": "metric",  # Celsius
            "lang": "vi"  # Vietnamese
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.base_url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return self._parse_weather_data(data)
                    else:
                        print(f"Weather API Error: {response.status}")
                        return None
        except Exception as e:
            print(f"Weather Service Error: {e}")
            return None
    
    def _parse_weather_data(self, data):
        """Parse raw API response into structured data"""
        try:
            weather = {
                "temperature": round(data["main"]["temp"], 1),
                "feels_like": round(data["main"]["feels_like"], 1),
                "humidity": data["main"]["humidity"],
                "pressure": data["main"]["pressure"],
                "description": data["weather"][0]["description"],
                "icon": data["weather"][0]["icon"],
                "wind_speed": round(data["wind"]["speed"] * 3.6, 1),  # m/s to km/h
                "wind_direction": self._get_wind_direction(data["wind"].get("deg", 0)),
                "clouds": data["clouds"]["all"],
                "visibility": data.get("visibility", 0) / 1000,  # meters to km
            }
            return weather
        except KeyError as e:
            print(f"Error parsing weather data: {e}")
            return None
    
    def _get_wind_direction(self, degrees):
        """Convert wind degrees to Vietnamese direction"""
        directions = ["Bắc", "Đông Bắc", "Đông", "Đông Nam", 
                     "Nam", "Tây Nam", "Tây", "Tây Bắc"]
        index = round(degrees / 45) % 8
        return directions[index]
