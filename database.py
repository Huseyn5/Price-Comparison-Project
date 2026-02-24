import sqlite3
import json
from datetime import datetime
from contextlib import contextmanager

DATABASE = "products.db"

@contextmanager
def get_db():
    """Context manager for database connections."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    """Initialize database with enhanced schema."""
    with get_db() as conn:
        c = conn.cursor()
        
        # Products table with enhanced fields
        c.execute('''CREATE TABLE IF NOT EXISTS products
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      name TEXT NOT NULL,
                      description TEXT,
                      category TEXT NOT NULL,
                      price REAL NOT NULL,
                      original_price REAL,
                      discount_percentage REAL DEFAULT 0,
                      store TEXT NOT NULL,
                      link TEXT NOT NULL,
                      image TEXT,
                      rating REAL DEFAULT 0,
                      availability TEXT DEFAULT 'in_stock',
                      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                      updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                      UNIQUE(name, store, price))''')
        
        # Stores table
        c.execute('''CREATE TABLE IF NOT EXISTS stores
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      name TEXT UNIQUE NOT NULL,
                      url TEXT,
                      logo TEXT)''')
        
        # Categories table
        c.execute('''CREATE TABLE IF NOT EXISTS categories
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      name TEXT UNIQUE NOT NULL,
                      description TEXT)''')
        
        # Comparison history table (for tracking user comparisons)
        c.execute('''CREATE TABLE IF NOT EXISTS comparisons
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      product_ids TEXT NOT NULL,
                      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
        
        conn.commit()

def insert_product(name, price, store, link, image, category="Electronics", 
                   description="", original_price=None, rating=0, availability="in_stock"):
    """Insert a product into the database."""
    try:
        with get_db() as conn:
            c = conn.cursor()
            discount = 0
            if original_price and original_price > price:
                discount = round(((original_price - price) / original_price) * 100, 2)
            
            c.execute('''INSERT INTO products 
                        (name, price, store, link, image, category, description, 
                         original_price, discount_percentage, rating, availability)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                     (name, price, store, link, image, category, description,
                      original_price, discount, rating, availability))
            conn.commit()
            return c.lastrowid
    except sqlite3.IntegrityError:
        # Product already exists
        return None

def get_all_products(limit=None, offset=0):
    """Get all products with pagination."""
    with get_db() as conn:
        c = conn.cursor()
        if limit:
            c.execute("SELECT * FROM products ORDER BY created_at DESC LIMIT ? OFFSET ?", 
                     (limit, offset))
        else:
            c.execute("SELECT * FROM products ORDER BY created_at DESC")
        rows = c.fetchall()
    return [dict(row) for row in rows]

def search_products(query, limit=50):
    """Search products by name or description."""
    with get_db() as conn:
        c = conn.cursor()
        search_term = f"%{query}%"
        c.execute('''SELECT * FROM products 
                     WHERE name LIKE ? OR description LIKE ? 
                     ORDER BY rating DESC, created_at DESC 
                     LIMIT ?''', (search_term, search_term, limit))
        rows = c.fetchall()
    return [dict(row) for row in rows]

def filter_products(category=None, min_price=None, max_price=None, 
                   store=None, min_rating=None, availability=None):
    """Filter products by various criteria."""
    with get_db() as conn:
        c = conn.cursor()
        query = "SELECT * FROM products WHERE 1=1"
        params = []
        
        if category:
            query += " AND category = ?"
            params.append(category)
        
        if min_price is not None:
            query += " AND price >= ?"
            params.append(min_price)
        
        if max_price is not None:
            query += " AND price <= ?"
            params.append(max_price)
        
        if store:
            query += " AND store = ?"
            params.append(store)
        
        if min_rating is not None:
            query += " AND rating >= ?"
            params.append(min_rating)
        
        if availability:
            query += " AND availability = ?"
            params.append(availability)
        
        query += " ORDER BY price ASC"
        c.execute(query, params)
        rows = c.fetchall()
    
    return [dict(row) for row in rows]

def get_product_by_id(product_id):
    """Get a single product by ID."""
    with get_db() as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM products WHERE id = ?", (product_id,))
        row = c.fetchone()
    return dict(row) if row else None

def get_products_by_ids(product_ids):
    """Get multiple products by IDs for comparison."""
    if not product_ids:
        return []
    
    with get_db() as conn:
        c = conn.cursor()
        placeholders = ','.join('?' * len(product_ids))
        c.execute(f"SELECT * FROM products WHERE id IN ({placeholders})", product_ids)
        rows = c.fetchall()
    return [dict(row) for row in rows]

def get_all_stores():
    """Get all unique stores."""
    with get_db() as conn:
        c = conn.cursor()
        c.execute("SELECT DISTINCT store FROM products ORDER BY store")
        rows = c.fetchall()
    return [row[0] for row in rows]

def get_all_categories():
    """Get all unique categories."""
    with get_db() as conn:
        c = conn.cursor()
        c.execute("SELECT DISTINCT category FROM products ORDER BY category")
        rows = c.fetchall()
    return [row[0] for row in rows]

def get_products_by_store(store):
    """Get all products from a specific store."""
    with get_db() as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM products WHERE store = ? ORDER BY price ASC", (store,))
        rows = c.fetchall()
    return [dict(row) for row in rows]

def get_products_by_category(category):
    """Get all products in a specific category."""
    with get_db() as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM products WHERE category = ? ORDER BY rating DESC", (category,))
        rows = c.fetchall()
    return [dict(row) for row in rows]

def get_price_comparison(product_name):
    """Get price comparison for a specific product across all stores."""
    with get_db() as conn:
        c = conn.cursor()
        c.execute('''SELECT store, price, link FROM products 
                     WHERE name LIKE ? 
                     ORDER BY price ASC''', (f"%{product_name}%",))
        rows = c.fetchall()
    return [dict(row) for row in rows]

def update_product(product_id, **kwargs):
    """Update product fields."""
    allowed_fields = {'name', 'description', 'price', 'original_price', 
                     'discount_percentage', 'rating', 'availability', 'image'}
    
    fields_to_update = {k: v for k, v in kwargs.items() if k in allowed_fields}
    
    if not fields_to_update:
        return False
    
    fields_to_update['updated_at'] = datetime.now().isoformat()
    
    with get_db() as conn:
        c = conn.cursor()
        set_clause = ', '.join([f"{k} = ?" for k in fields_to_update.keys()])
        values = list(fields_to_update.values()) + [product_id]
        
        c.execute(f"UPDATE products SET {set_clause} WHERE id = ?", values)
        conn.commit()
        return c.rowcount > 0

def delete_product(product_id):
    """Delete a product by ID."""
    with get_db() as conn:
        c = conn.cursor()
        c.execute("DELETE FROM products WHERE id = ?", (product_id,))
        conn.commit()
        return c.rowcount > 0

def get_statistics():
    """Get database statistics."""
    with get_db() as conn:
        c = conn.cursor()
        
        c.execute("SELECT COUNT(*) FROM products")
        total_products = c.fetchone()[0]
        
        c.execute("SELECT COUNT(DISTINCT store) FROM products")
        total_stores = c.fetchone()[0]
        
        c.execute("SELECT COUNT(DISTINCT category) FROM products")
        total_categories = c.fetchone()[0]
        
        c.execute("SELECT AVG(price) FROM products")
        avg_price = c.fetchone()[0]
        
        c.execute("SELECT MIN(price), MAX(price) FROM products")
        min_price, max_price = c.fetchone()
    
    return {
        "total_products": total_products,
        "total_stores": total_stores,
        "total_categories": total_categories,
        "average_price": round(avg_price, 2) if avg_price else 0,
        "min_price": min_price,
        "max_price": max_price
    }

# Initialize database on import
if __name__ == "__main__":
    init_db()
    print("Database initialized successfully!")
