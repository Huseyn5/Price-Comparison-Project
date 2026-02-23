from selenium import webdriver
from database import insert_product, init_db

# Example scraper (dummy data)

def search_for_product(driver, product_name):
    
    search_box = driver.find_element("name", "q")
    search_box.clear()
    search_box.send_keys(product_name)
    search_box.submit()
def scrape_dummy_products():
    products = [
        {"name": "iPhone 15 Pro 128GB", "price": 1199.99, "store": "BestBuy",
         "link": "https://www.bestbuy.ca/en-ca/product/iphone15pro",
         "image": "https://m.media-amazon.com/images/I/61XXUxrT1xL._AC_SY300_SX300_QL70_ML2_.jpg"}
        ,
        {"name": "MacBook Air M2 13-inch", "price": 1499.00, "store": "Apple",
         "link": "https://www.apple.com/macbook-air/",
         "image": "https://m.media-amazon.com/images/I/71se+LJZybL._AC_SX342_SY445_QL70_ML2_.jpg"}
        ,
        {"name": "Dell XPS 13 Laptop", "price": 1399.99, "store": "Dell",
         "link": "https://www.dell.com/xps-13",
         "image": "https://i.dell.com/is/image/DellContent/content/dam/ss2/product-images/dell-client-products/notebooks/xps-notebooks/xps-13-9350/media-gallery/platinum/notebook-xps-13-9350-t-oled-sl-gallery-1.psd?fmt=png-alpha&pscan=auto&scl=1&hei=402&wid=699&qlt=100,1&resMode=sharp2&size=699,402&chrss=full"}
    ]

    for p in products:
        insert_product(p["name"], p["price"], p["store"], p["link"], p["image"])
    print("Inserted dummy products into DB!")

def scrape_example():
    driver = webdriver.Chrome()
    driver.get("https://www.example.com")
    # TODO: extract product details
    driver.quit()

if __name__ == "__main__":
    init_db()
    scrape_dummy_products()

