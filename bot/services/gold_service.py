"""
Gold price service to fetch SJC gold prices from VNAppMob vAPI
"""
import aiohttp

class GoldService:
    def __init__(self, api_key):
        self.api_key = api_key
        # Try multiple sources - PNJ first, fallback to SJC if PNJ is empty
        self.endpoints = [
            ("PNJ", "https://api.vnappmob.com/api/v2/gold/pnj"),
            ("SJC", "https://api.vnappmob.com/api/v2/gold/sjc"),
            ("DOJI", "https://api.vnappmob.com/api/v2/gold/doji"),
        ]

        
    async def get_gold_price(self):
        """
        Fetch gold prices - tries PNJ first, falls back to SJC/DOJI if needed
        Returns: dict with gold price information or None if all sources fail
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        
        # Try each endpoint in order
        for brand, url in self.endpoints:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url, headers=headers) as response:
                        print(f"Gold API ({brand}) Status: {response.status}")
                        if response.status == 200:
                            response_text = await response.text()
                            print(f"Gold API ({brand}) Response: {response_text[:200]}")
                            data = await response.json()
                            print(f"Gold API ({brand}) Data: {data}")
                            
                            # Check if data is not empty
                            if data.get("results") and len(data["results"]) > 0:
                                parsed = self._parse_gold_data(data, brand)
                                if parsed:
                                    print(f"✅ Using {brand} gold prices")
                                    return parsed
                            else:
                                print(f"⚠️ {brand} endpoint returned empty results, trying next source...")
            except Exception as e:
                print(f"Gold Service Error ({brand}): {e}")
                continue
        
        # All sources failed
        print("❌ All gold price sources failed")
        return None
    
    def _parse_gold_data(self, data, brand="SJC"):
        """Parse raw API response into structured data"""
        try:
            # vAPI returns data in format with 'results' key containing list of gold types
            if "results" in data and len(data["results"]) > 0:
                # Look for SJC vàng 9999 or first entry
                gold_data = None
                for item in data["results"]:
                    brand = item.get("brand", "").upper()
                    if "SJC" in brand or "9999" in item.get("type", ""):
                        gold_data = item
                        break
                
                if not gold_data:
                    gold_data = data["results"][0]  # Fallback to first item
                
                # Use SJC gold bar 1 luong (1 tael) prices - this is what newspapers report
                buy_price = gold_data.get("buy_1l", "0")  # Mua vàng miếng 1 lượng
                sell_price = gold_data.get("sell_1l", "0")  # Bán vàng miếng 1 lượng
                
                print(f"DEBUG: Raw buy_1l = {buy_price}, sell_1l = {sell_price}")
                
                # Convert to float then to integer (remove decimals)
                try:
                    buy_formatted = int(float(buy_price)) // 1000  # Convert to thousands
                    sell_formatted = int(float(sell_price)) // 1000
                except:
                    buy_formatted = 0
                    sell_formatted = 0
                
                print(f"DEBUG: Formatted buy = {buy_formatted:,}, sell = {sell_formatted:,}")
                
                # Parse datetime (Unix timestamp)
                updated_time = ""
                if "datetime" in gold_data:
                    try:
                        from datetime import datetime
                        timestamp = int(gold_data["datetime"])
                        dt = datetime.fromtimestamp(timestamp)
                        updated_time = dt.strftime("%d/%m/%Y %H:%M")
                    except:
                        updated_time = ""
                
                gold = {
                    "type": f"{brand} Vàng miếng 1L",
                    "buy": f"{buy_formatted:,}",
                    "sell": f"{sell_formatted:,}",
                    "updated": updated_time
                }
                return gold
            return None
        except Exception as e:
            print(f"Error parsing gold data: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _format_price(self, price):
        """Format price with thousand separators"""
        try:
            # Price is usually in thousands (e.g., 87500 = 87,500,000 VND)
            return f"{price:,}"
        except:
            return str(price)
