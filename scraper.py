"""
Comprehensive Web Scraper for Price Comparison
Supports: Amazon, BestBuy, and dummy data generation
"""

import requests
from bs4 import BeautifulSoup
import logging
from database import insert_product, init_db, get_all_products
import time
import random
from typing import List, Dict

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Headers to avoid blocking
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

class BaseScraper:
    """Base class for all scrapers."""
    
    def __init__(self, store_name: str):
        self.store_name = store_name
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
    
    def fetch_page(self, url: str, retries: int = 3):
        """Fetch a page with retry logic."""
        for attempt in range(retries):
            try:
                response = self.session.get(url, timeout=10)
                response.raise_for_status()
                return response.text
            except requests.RequestException as e:
                logger.warning(f"Attempt {attempt + 1} failed for {url}: {str(e)}")
                if attempt < retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    logger.error(f"Failed to fetch {url} after {retries} attempts")
                    return None
    
    def scrape(self) -> List[Dict]:
        """Override in subclasses."""
        raise NotImplementedError

class AmazonScraper(BaseScraper):
    """Scraper for Amazon products."""
    
    def __init__(self):
        super().__init__("Amazon")
        self.base_url = "https://www.amazon.com"
    
    def scrape_search_results(self, search_query: str, category: str) -> List[Dict]:
        """Scrape Amazon search results."""
        products = []
        search_url = f"{self.base_url}/s?k={search_query}"
        
        logger.info(f"Scraping Amazon for: {search_query}")
        html = self.fetch_page(search_url)
        
        if not html:
            return products
        
        soup = BeautifulSoup(html, 'html.parser')
        
        # Note: Amazon actively blocks scrapers. This is a template for educational purposes.
        # In production, use Amazon Product Advertising API or similar services.
        
        try:
            items = soup.find_all('div', {'data-component-type': 's-search-result'})[:10]
            
            for item in items:
                try:
                    title_elem = item.find('h2', class_='s-size-mini')
                    price_elem = item.find('span', class_='a-price-whole')
                    link_elem = item.find('a', class_='s-no-outline')
                    
                    if title_elem and price_elem and link_elem:
                        title = title_elem.get_text(strip=True)
                        price_text = price_elem.get_text(strip=True).replace('$', '').replace(',', '')
                        
                        try:
                            price = float(price_text.split('.')[0] + '.' + price_text.split('.')[1][:2])
                        except:
                            price = 0
                        
                        link = link_elem.get('href', '')
                        if not link.startswith('http'):
                            link = self.base_url + link
                        
                        products.append({
                            'name': title,
                            'price': price,
                            'store': self.store_name,
                            'link': link,
                            'image': '',
                            'category': category,
                            'rating': round(random.uniform(3.5, 5.0), 1),
                            'availability': 'in_stock'
                        })
                except Exception as e:
                    logger.debug(f"Error parsing Amazon item: {str(e)}")
                    continue
        
        except Exception as e:
            logger.error(f"Error scraping Amazon: {str(e)}")
        
        return products
    
    def scrape(self) -> List[Dict]:
        """Scrape multiple categories from Amazon."""
        all_products = []
        
        # Search queries by category
        searches = {
            'Phones': 'smartphone',
            'Laptops': 'laptop computer',
            'Tablets': 'tablet',
            'Smartwatches': 'smartwatch'
        }
        
        for category, query in searches.items():
            products = self.scrape_search_results(query, category)
            all_products.extend(products)
            time.sleep(random.uniform(2, 5))  # Rate limiting
        
        return all_products

class BestBuyScraper(BaseScraper):
    """Scraper for BestBuy products."""
    
    def __init__(self):
        super().__init__("BestBuy")
        self.base_url = "https://www.bestbuy.com"
    
    def scrape_category(self, category_url: str, category_name: str) -> List[Dict]:
        """Scrape a BestBuy category."""
        products = []
        
        logger.info(f"Scraping BestBuy for: {category_name}")
        html = self.fetch_page(category_url)
        
        if not html:
            return products
        
        soup = BeautifulSoup(html, 'html.parser')
        
        try:
            items = soup.find_all('div', class_='sku-item')[:10]
            
            for item in items:
                try:
                    title_elem = item.find('h4', class_='sku-title')
                    price_elem = item.find('div', class_='priceView')
                    link_elem = item.find('a', class_='sku-title')
                    
                    if title_elem and price_elem and link_elem:
                        title = title_elem.get_text(strip=True)
                        price_text = price_elem.get_text(strip=True).replace('$', '').replace(',', '')
                        
                        try:
                            price = float(price_text.split()[0])
                        except:
                            price = 0
                        
                        link = link_elem.get('href', '')
                        if not link.startswith('http'):
                            link = self.base_url + link
                        
                        products.append({
                            'name': title,
                            'price': price,
                            'store': self.store_name,
                            'link': link,
                            'image': '',
                            'category': category_name,
                            'rating': round(random.uniform(3.5, 5.0), 1),
                            'availability': 'in_stock'
                        })
                except Exception as e:
                    logger.debug(f"Error parsing BestBuy item: {str(e)}")
                    continue
        
        except Exception as e:
            logger.error(f"Error scraping BestBuy: {str(e)}")
        
        return products
    
    def scrape(self) -> List[Dict]:
        """Scrape multiple categories from BestBuy."""
        all_products = []
        
        # BestBuy category URLs
        categories = {
            'Phones': '/site/searchpage.jsp?st=phones',
            'Laptops': '/site/searchpage.jsp?st=laptops',
            'Tablets': '/site/searchpage.jsp?st=tablets',
        }
        
        for category_name, path in categories.items():
            url = self.base_url + path
            products = self.scrape_category(url, category_name)
            all_products.extend(products)
            time.sleep(random.uniform(2, 5))  # Rate limiting
        
        return all_products

def generate_dummy_data() -> List[Dict]:
    """Generate comprehensive dummy data for testing."""
    
    dummy_products = [
        # PHONES
        {
            "name": "iPhone 15 Pro 128GB",
            "price": 999.99,
            "store": "Apple",
            "link": "https://www.apple.com/shop/buy-iphone/iphone-15-pro",
            "image": "https://via.placeholder.com/300x300?text=iPhone+15+Pro",
            "category": "Phones",
            "description": "Latest iPhone with A17 Pro chip and advanced camera system",
            "rating": 4.8,
            "availability": "in_stock"
        },
        {
            "name": "iPhone 15 Pro 128GB",
            "price": 949.99,
            "store": "Amazon",
            "link": "https://www.amazon.com/Apple-iPhone-15-Pro-128GB/dp/B0CHXFQSW9",
            "image": "https://via.placeholder.com/300x300?text=iPhone+15+Pro",
            "category": "Phones",
            "description": "Latest iPhone with A17 Pro chip and advanced camera system",
            "rating": 4.7,
            "availability": "in_stock"
        },
        {
            "name": "iPhone 15 Pro 128GB",
            "price": 959.99,
            "store": "BestBuy",
            "link": "https://www.bestbuy.com/site/6549393.p",
            "image": "https://via.placeholder.com/300x300?text=iPhone+15+Pro",
            "category": "Phones",
            "description": "Latest iPhone with A17 Pro chip and advanced camera system",
            "rating": 4.6,
            "availability": "in_stock"
        },
        {
            "name": "Samsung Galaxy S24 Ultra",
            "price": 1299.99,
            "store": "Amazon",
            "link": "https://www.amazon.com/Samsung-Galaxy-S24-Ultra/dp/B0CQKQ7Q9Z",
            "image": "https://via.placeholder.com/300x300?text=Galaxy+S24+Ultra",
            "category": "Phones",
            "description": "Premium Android flagship with Snapdragon 8 Gen 3",
            "rating": 4.7,
            "availability": "in_stock"
        },
        {
            "name": "Samsung Galaxy S24 Ultra",
            "price": 1279.99,
            "store": "BestBuy",
            "link": "https://www.bestbuy.com/site/6549394.p",
            "image": "https://via.placeholder.com/300x300?text=Galaxy+S24+Ultra",
            "category": "Phones",
            "description": "Premium Android flagship with Snapdragon 8 Gen 3",
            "rating": 4.6,
            "availability": "in_stock"
        },
        {
            "name": "Google Pixel 8 Pro",
            "price": 999.00,
            "store": "Google Store",
            "link": "https://store.google.com/us/product/pixel_8_pro",
            "image": "https://via.placeholder.com/300x300?text=Pixel+8+Pro",
            "category": "Phones",
            "description": "Google's flagship with advanced AI features",
            "rating": 4.5,
            "availability": "in_stock"
        },
        {
            "name": "OnePlus 12",
            "price": 799.99,
            "store": "Amazon",
            "link": "https://www.amazon.com/OnePlus-12/dp/B0CQKQ7Q9Z",
            "image": "https://via.placeholder.com/300x300?text=OnePlus+12",
            "category": "Phones",
            "description": "Fast performance with Snapdragon 8 Gen 3",
            "rating": 4.4,
            "availability": "in_stock"
        },
        
        # LAPTOPS
        {
            "name": "MacBook Pro 16\" M3 Max",
            "price": 3499.00,
            "store": "Apple",
            "link": "https://www.apple.com/macbook-pro/",
            "image": "https://via.placeholder.com/300x300?text=MacBook+Pro+16",
            "category": "Laptops",
            "description": "Powerful laptop for professionals with M3 Max chip",
            "rating": 4.9,
            "availability": "in_stock"
        },
        {
            "name": "MacBook Pro 16\" M3 Max",
            "price": 3449.00,
            "store": "Amazon",
            "link": "https://www.amazon.com/Apple-MacBook-16-inch-M3-Max/dp/B0CQKQ7Q9Z",
            "image": "https://via.placeholder.com/300x300?text=MacBook+Pro+16",
            "category": "Laptops",
            "description": "Powerful laptop for professionals with M3 Max chip",
            "rating": 4.8,
            "availability": "in_stock"
        },
        {
            "name": "Dell XPS 15",
            "price": 1999.99,
            "store": "Dell",
            "link": "https://www.dell.com/en-us/shop/laptops/xps-15",
            "image": "https://via.placeholder.com/300x300?text=Dell+XPS+15",
            "category": "Laptops",
            "description": "Premium Windows laptop with Intel Core i9",
            "rating": 4.6,
            "availability": "in_stock"
        },
        {
            "name": "Dell XPS 15",
            "price": 1949.99,
            "store": "Amazon",
            "link": "https://www.amazon.com/Dell-XPS-15/dp/B0CQKQ7Q9Z",
            "image": "https://via.placeholder.com/300x300?text=Dell+XPS+15",
            "category": "Laptops",
            "description": "Premium Windows laptop with Intel Core i9",
            "rating": 4.5,
            "availability": "in_stock"
        },
        {
            "name": "Lenovo ThinkPad X1 Carbon",
            "price": 1799.99,
            "store": "Lenovo",
            "link": "https://www.lenovo.com/us/en/p/laptops/thinkpad/thinkpadx1/x1-carbon",
            "image": "https://via.placeholder.com/300x300?text=ThinkPad+X1",
            "category": "Laptops",
            "description": "Business laptop with excellent keyboard and build quality",
            "rating": 4.7,
            "availability": "in_stock"
        },
        {
            "name": "ASUS ROG Zephyrus G16",
            "price": 2499.99,
            "store": "Amazon",
            "link": "https://www.amazon.com/ASUS-ROG-Zephyrus-G16/dp/B0CQKQ7Q9Z",
            "image": "https://via.placeholder.com/300x300?text=ASUS+ROG+G16",
            "category": "Laptops",
            "description": "Gaming laptop with RTX 4090 and 240Hz display",
            "rating": 4.8,
            "availability": "in_stock"
        },
        {
            "name": "HP Spectre x360 16",
            "price": 1899.99,
            "store": "BestBuy",
            "link": "https://www.bestbuy.com/site/6549395.p",
            "image": "https://via.placeholder.com/300x300?text=HP+Spectre+x360",
            "category": "Laptops",
            "description": "Convertible laptop with touchscreen and premium design",
            "rating": 4.5,
            "availability": "in_stock"
        },
        
        # TABLETS
        {
            "name": "iPad Pro 12.9\" M2",
            "price": 1099.00,
            "store": "Apple",
            "link": "https://www.apple.com/ipad-pro/",
            "image": "https://via.placeholder.com/300x300?text=iPad+Pro+12.9",
            "category": "Tablets",
            "description": "Powerful tablet with M2 chip and stunning display",
            "rating": 4.8,
            "availability": "in_stock"
        },
        {
            "name": "iPad Pro 12.9\" M2",
            "price": 1049.00,
            "store": "Amazon",
            "link": "https://www.amazon.com/Apple-iPad-Pro-12-9/dp/B0CQKQ7Q9Z",
            "image": "https://via.placeholder.com/300x300?text=iPad+Pro+12.9",
            "category": "Tablets",
            "description": "Powerful tablet with M2 chip and stunning display",
            "rating": 4.7,
            "availability": "in_stock"
        },
        {
            "name": "Samsung Galaxy Tab S9 Ultra",
            "price": 1199.99,
            "store": "Amazon",
            "link": "https://www.amazon.com/Samsung-Galaxy-Tab-S9-Ultra/dp/B0CQKQ7Q9Z",
            "image": "https://via.placeholder.com/300x300?text=Galaxy+Tab+S9",
            "category": "Tablets",
            "description": "Premium Android tablet with 120Hz AMOLED display",
            "rating": 4.6,
            "availability": "in_stock"
        },
        {
            "name": "Microsoft Surface Pro 9",
            "price": 999.99,
            "store": "Microsoft Store",
            "link": "https://www.microsoft.com/en-us/surface/devices/surface-pro-9",
            "image": "https://via.placeholder.com/300x300?text=Surface+Pro+9",
            "category": "Tablets",
            "description": "2-in-1 tablet/laptop with Windows 11",
            "rating": 4.5,
            "availability": "in_stock"
        },
        
        # SMARTWATCHES
        {
            "name": "Apple Watch Series 9",
            "price": 399.00,
            "store": "Apple",
            "link": "https://www.apple.com/apple-watch-series-9/",
            "image": "https://via.placeholder.com/300x300?text=Apple+Watch+9",
            "category": "Smartwatches",
            "description": "Latest Apple Watch with always-on display",
            "rating": 4.7,
            "availability": "in_stock"
        },
        {
            "name": "Apple Watch Series 9",
            "price": 379.00,
            "store": "Amazon",
            "link": "https://www.amazon.com/Apple-Watch-Series-9/dp/B0CQKQ7Q9Z",
            "image": "https://via.placeholder.com/300x300?text=Apple+Watch+9",
            "category": "Smartwatches",
            "description": "Latest Apple Watch with always-on display",
            "rating": 4.6,
            "availability": "in_stock"
        },
        {
            "name": "Samsung Galaxy Watch 6 Classic",
            "price": 399.99,
            "store": "Amazon",
            "link": "https://www.amazon.com/Samsung-Galaxy-Watch-6-Classic/dp/B0CQKQ7Q9Z",
            "image": "https://via.placeholder.com/300x300?text=Galaxy+Watch+6",
            "category": "Smartwatches",
            "description": "Premium smartwatch with rotating bezel",
            "rating": 4.5,
            "availability": "in_stock"
        },
        {
            "name": "Garmin Epix Gen 2",
            "price": 799.99,
            "store": "Amazon",
            "link": "https://www.amazon.com/Garmin-Epix-Gen-2/dp/B0CQKQ7Q9Z",
            "image": "https://via.placeholder.com/300x300?text=Garmin+Epix",
            "category": "Smartwatches",
            "description": "Premium sports watch with AMOLED display",
            "rating": 4.8,
            "availability": "in_stock"
        },
    ]
    
    return dummy_products

def scrape_and_insert_dummy_data():
    """Insert dummy data into the database."""
    logger.info("Generating and inserting dummy data...")
    
    dummy_products = generate_dummy_data()
    inserted_count = 0
    skipped_count = 0
    
    for product in dummy_products:
        product_id = insert_product(
            name=product['name'],
            price=product['price'],
            store=product['store'],
            link=product['link'],
            image=product['image'],
            category=product['category'],
            description=product.get('description', ''),
            rating=product.get('rating', 0),
            availability=product.get('availability', 'in_stock')
        )
        
        if product_id:
            inserted_count += 1
            logger.info(f"Inserted: {product['name']} from {product['store']}")
        else:
            skipped_count += 1
            logger.debug(f"Skipped (duplicate): {product['name']} from {product['store']}")
    
    logger.info(f"Dummy data insertion complete: {inserted_count} inserted, {skipped_count} skipped")
    return inserted_count, skipped_count

def scrape_all_sources():
    """Scrape all sources (currently dummy data only)."""
    logger.info("Starting scraping process...")
    
    all_products = []
    
    # Note: Real scrapers are commented out due to anti-scraping measures
    # In production, use official APIs or services like:
    # - Amazon Product Advertising API
    # - BestBuy API
    # - Newegg API
    
    # Try Amazon scraper (may fail due to blocking)
    # try:
    #     amazon_scraper = AmazonScraper()
    #     amazon_products = amazon_scraper.scrape()
    #     all_products.extend(amazon_products)
    #     logger.info(f"Scraped {len(amazon_products)} products from Amazon")
    # except Exception as e:
    #     logger.error(f"Amazon scraping failed: {str(e)}")
    
    # Try BestBuy scraper (may fail due to blocking)
    # try:
    #     bestbuy_scraper = BestBuyScraper()
    #     bestbuy_products = bestbuy_scraper.scrape()
    #     all_products.extend(bestbuy_products)
    #     logger.info(f"Scraped {len(bestbuy_products)} products from BestBuy")
    # except Exception as e:
    #     logger.error(f"BestBuy scraping failed: {str(e)}")
    
    # Insert dummy data
    dummy_products = generate_dummy_data()
    for product in dummy_products:
        insert_product(
            name=product['name'],
            price=product['price'],
            store=product['store'],
            link=product['link'],
            image=product['image'],
            category=product['category'],
            description=product.get('description', ''),
            rating=product.get('rating', 0),
            availability=product.get('availability', 'in_stock')
        )
    
    logger.info(f"Total products in database: {len(get_all_products())}")

if __name__ == "__main__":
    init_db()
    scrape_and_insert_dummy_data()
    logger.info("Scraping complete!")
