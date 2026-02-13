"""
Forex (Foreign Exchange) Service - fetches AUD and other currency rates
Scrapes from Vietcombank official exchange rate page
"""
import aiohttp
from bs4 import BeautifulSoup
import re

class ForexService:
    def __init__(self):
        self.base_url = "https://portal.vietcombank.com.vn/UserControls/TVPortal.TyGia/pXML.aspx"
    
    async def get_aud_rates(self):
        """
        Fetch AUD exchange rates from Vietcombank
        Returns: dict with buy/transfer/sell rates
        """
        try:
            async with aiohttp.ClientSession() as session:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
                async with session.get(self.base_url, headers=headers) as response:
                    if response.status == 200:
                        xml_text = await response.text()
                        return self._parse_aud_data(xml_text)
                    else:
                        print(f"AUD API Error: {response.status}")
                        return None
        except Exception as e:
            print(f"AUD Service Error: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _parse_aud_data(self, xml_text):
        """Parse XML to extract AUD rates"""
        try:
            soup = BeautifulSoup(xml_text, 'xml')
            
            aud_data = {
                "buy": "0",
                "transfer": "0",
                "sell": "0",
                "source": "Vietcombank"
            }
            
            # Find AUD entry in XML
            # XML format: <Exrate CurrencyCode="AUD" CurrencyName="AUD" Buy="17923.63" Transfer="18104.68" Sell="18684.85"/>
            aud_node = soup.find('Exrate', {'CurrencyCode': 'AUD'})
            
            if aud_node:
                buy = aud_node.get('Buy', '0')
                transfer = aud_node.get('Transfer', '0')
                sell = aud_node.get('Sell', '0')
                
                # Remove commas and format
                aud_data["buy"] = buy.replace(',', '')
                aud_data["transfer"] = transfer.replace(',', '')
                aud_data["sell"] = sell.replace(',', '')
            
            print(f"Parsed AUD data: {aud_data}")
            return aud_data
            
        except Exception as e:
            print(f"Error parsing AUD data: {e}")
            import traceback
            traceback.print_exc()
            return None
