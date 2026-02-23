import sqlite3

def init_db():
    conn = sqlite3.connect("products.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS products
                 (id INTEGER PRIMARY KEY,
                  name TEXT,
                  price REAL,
                  store TEXT,
                  link TEXT,
                  image TEXT)''')   # 👈 add image column
    conn.commit()
    conn.close()

def get_all_products():
    conn = sqlite3.connect("products.db")
    c = conn.cursor()
    c.execute("SELECT * FROM products")
    rows = c.fetchall()
    conn.close()
    return [{"id": r[0], "name": r[1], "price": r[2], "store": r[3], "link": r[4], "image": r[5]} for r in rows]

def insert_product(name, price, store, link, image):
    conn = sqlite3.connect("products.db")
    c = conn.cursor()
    c.execute("INSERT INTO products (name, price, store, link, image) VALUES (?, ?, ?, ?, ?)",
              (name, price, store, link, image))
    conn.commit()
    conn.close()

# Run once to create DB
# if __name__ == "__main__":
#     init_db()
