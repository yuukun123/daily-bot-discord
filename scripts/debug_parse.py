from bs4 import BeautifulSoup
import re

# Read the saved HTML file
with open('tygiausd_page.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

# Debug: find black market section
print("Looking for black market rates...")
print("="*60)

black_market_row = soup.find(string=re.compile(r'USD chợ đen', re.I))
print(f"Found black_market_row: {black_market_row}")

if black_market_row:
    row = black_market_row.find_parent('tr')
    print(f"\nFound row: {row}")
    
    if row:
        cells = row.find_all('td', class_='text-right')
        print(f"\nFound {len(cells)} cells with class='text-right'")
        
        for i, cell in enumerate(cells):
            print(f"Cell {i}: {cell.get_text(strip=True)}")
