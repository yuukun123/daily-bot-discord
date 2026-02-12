import aiohttp
import asyncio

async def fetch_html():
    url = "https://tygiausd.org/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            html = await response.text()
            
            # Save HTML to file for inspection
            with open('tygiausd_page.html', 'w', encoding='utf-8') as f:
                f.write(html)
            
            print("HTML saved to tygiausd_page.html")
            print("\nFirst 2000 characters:")
            print("="*60)
            print(html[:2000])

asyncio.run(fetch_html())
