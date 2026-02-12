"""
USD Exchange Rate Service - scrapes from tygiausd.org
Fetches both bank rates and black market rates
"""
import aiohttp
from bs4 import BeautifulSoup
import re

class USDService:
    def __init__(self):
        self.base_url = "https://tygiausd.org/"
    
    async def get_usd_rates(self):
        """
        Fetch USD exchange rates from tygiausd.org
        Returns: dict with bank rates and black market rates
        """
        try:
            async with aiohttp.ClientSession() as session:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
                async with session.get(self.base_url, headers=headers) as response:
                    if response.status == 200:
                        html = await response.text()
                        return self._parse_usd_data(html)
                    else:
                        print(f"USD API Error: {response.status}")
                        return None
        except Exception as e:
            print(f"USD Service Error: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _parse_usd_data(self, html):
        """Parse HTML to extract USD rates"""
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            usd_data = {
                "bank": {
                    "buy": "0",
                    "transfer": "0",
                    "sell": "0",
                    "source": "Vietcombank"
                },
                "black_market": {
                    "buy": "0",
                    "sell": "0"
                },
                "updated": ""
            }
            
            # Find black market rates - look for h3 with "USD chợ đen"
            black_market_h3 = soup.find('h3', string=re.compile(r'USD chợ đen', re.I))
            if black_market_h3:
                row = black_market_h3.find_parent('tr')
                if row:
                    cells = row.find_all('td', class_='text-right')
                    if len(cells) >= 2:
                        # Extract numbers, remove commas and extra text
                        buy_text = cells[0].get_text(strip=True)
                        sell_text = cells[1].get_text(strip=True)
                        
                        # Extract just the number before any span
                        buy_match = re.search(r'([\d,]+)', buy_text)
                        sell_match = re.search(r'([\d,]+)', sell_text)
                        
                        if buy_match:
                            usd_data["black_market"]["buy"] = buy_match.group(1).replace(',', '')
                        if sell_match:
                            usd_data["black_market"]["sell"] = sell_match.group(1).replace(',', '')

            
            # Find Vietcombank rates - in main table with USD row
            usd_row = soup.find('a', href='/ngoaite/usd')
            if usd_row:
                row = usd_row.find_parent('tr')
                if row:
                    cells = row.find_all('td', class_='text-right')
                    if len(cells) >= 3:
                        buy_text = cells[0].get_text(strip=True)
                        transfer_text = cells[1].get_text(strip=True)
                        sell_text = cells[2].get_text(strip=True)
                        
                        buy_match = re.search(r'([\d,]+)', buy_text)
                        transfer_match = re.search(r'([\d,]+)', transfer_text)
                        sell_match = re.search(r'([\d,]+)', sell_text)
                        
                        if buy_match:
                            usd_data["bank"]["buy"] = buy_match.group(1).replace(',', '')
                        if transfer_match:
                            usd_data["bank"]["transfer"] = transfer_match.group(1).replace(',', '')
                        if sell_match:
                            usd_data["bank"]["sell"] = sell_match.group(1).replace(',', '')
            
            print(f"Parsed USD data: {usd_data}")
            return usd_data
            
        except Exception as e:
            print(f"Error parsing USD data: {e}")
            import traceback
            traceback.print_exc()
            return None
