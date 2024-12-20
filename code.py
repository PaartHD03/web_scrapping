import requests
from bs4 import BeautifulSoup
import csv  


baseurl = 'https://www.noon.com/uae-en/sports-and-outdoors/exercise-and-fitness/yoga-16328/?page='
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
}


def extract_product_details(product, rank):
    try:
        
        product_name_div = product.find('div', {'data-qa': 'product-name'})
        product_name = product_name_div.text.strip() if product_name_div else None
        
        
        product_id = product_name_div.find_parent('a')['href'].split('/')[4] if product_name_div else None
        
        
        site_link = f"https://www.noon.com/uae-en/{product_name.replace(' ', '-').lower()}/{product_id}/p/?o={product_id}-1" if product_id else None
        
        
        price = product.find('strong', class_='amount').text.strip() if product.find('strong', class_='amount') else None
        
        
        old_price = product.find('span', class_='oldPrice').text.strip() if product.find('span', class_='oldPrice') else None
        
        
        discount = product.find('span', class_='discount').text.strip() if product.find('span', class_='discount') else None
        
        
        rating = product.find('div', class_='sc-9cb63f72-2 dGLdNc').text.strip() if product.find('div', class_='sc-9cb63f72-2 dGLdNc') else None
        
        
        rating_count = product.find('span', class_='sc-9cb63f72-5 DkxLK').text.strip() if product.find('span', class_='sc-9cb63f72-5 DkxLK') else None
        
        
        sponsored = 'y' if product.find('div', class_='sc-95ea18ef-24 gzboVs') else 'n'
        
        
        express_image = product.find('img', alt='noon-express')  
        express = 'y' if express_image else 'n'
        
        
        return {
            'Rank': rank,
            'Name': product_name,
            'Site Link': site_link,
            'Price': price,
            'Old Price': old_price,
            'Discount': discount,
            'Rating': rating,
            'Rating Count': rating_count,
            'Sponsored': sponsored,
            'Express': express
        }
    except Exception as e:
        print(f"Error extracting product: {e}")
        return None


def fetch_products(page_number):
    url = f"{baseurl}{page_number}"
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, 'lxml')
    
    
    productlist = soup.find_all('div', {'class': 'sc-57fe1f38-1'})  # Corrected to the div containing product info
    
    
    products = []
    rank = 1  
    for product in productlist:
        product_details = extract_product_details(product, rank)
        if product_details:
            products.append(product_details)
        rank += 1  
    
    return products


def scrape_until_200():
    all_products = []
    page_number = 1
    while len(all_products) < 200:
        print(f"Scraping page {page_number}...")
        products = fetch_products(page_number)
        
        
        if not products:
            print("No more products found. Ending scraping.")
            break
        
        all_products.extend(products)
        
        
        if len(all_products) >= 200:
            all_products = all_products[:200]  
        
        page_number += 1
    
    return all_products


products = scrape_until_200()


with open('noon_products_with_details.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Rank', 'Name', 'Site Link', 'Price', 'Old Price', 'Discount', 'Rating', 'Rating Count', 'Sponsored', 'Express']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    
    writer.writeheader()
    
    
    for product in products:
        writer.writerow(product)

print("Data has been saved to 'noon_products_with_details.csv'.")
