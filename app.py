from flask import Flask, jsonify, request
from flask_cors import CORS
from functools import wraps
import logging
from database import (
    init_db, get_all_products, search_products, filter_products,
    get_product_by_id, get_products_by_ids, get_all_stores, 
    get_all_categories, get_products_by_store, get_products_by_category,
    get_price_comparison, update_product, delete_product, get_statistics,
    insert_product
)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize database
init_db()

# ==================== MIDDLEWARE ====================

def handle_errors(f):
    """Decorator to handle errors in API endpoints."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            logger.error(f"Error in {f.__name__}: {str(e)}")
            return jsonify({"error": "Internal server error"}), 500
    return decorated_function

def validate_pagination(f):
    """Decorator to validate pagination parameters."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        limit = request.args.get('limit', 50, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        if limit < 1 or limit > 500:
            limit = 50
        if offset < 0:
            offset = 0
        
        kwargs['limit'] = limit
        kwargs['offset'] = offset
        return f(*args, **kwargs)
    return decorated_function

# ==================== HEALTH CHECK ====================

@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint."""
    return jsonify({"status": "healthy", "service": "PriceCompare API"}), 200

# ==================== PRODUCTS ENDPOINTS ====================

@app.route("/products", methods=["GET"])
@handle_errors
@validate_pagination
def get_products(limit, offset):
    """Get all products with pagination."""
    products = get_all_products(limit=limit, offset=offset)
    stats = get_statistics()
    
    return jsonify({
        "data": products,
        "pagination": {
            "limit": limit,
            "offset": offset,
            "total": stats["total_products"]
        }
    }), 200

@app.route("/products/<int:product_id>", methods=["GET"])
@handle_errors
def get_product_detail(product_id):
    """Get a single product by ID."""
    product = get_product_by_id(product_id)
    
    if not product:
        return jsonify({"error": "Product not found"}), 404
    
    return jsonify(product), 200

@app.route("/products/search", methods=["GET"])
@handle_errors
def search():
    """Search products by query."""
    query = request.args.get('q', '').strip()
    
    if not query or len(query) < 2:
        return jsonify({"error": "Search query must be at least 2 characters"}), 400
    
    limit = request.args.get('limit', 50, type=int)
    products = search_products(query, limit=limit)
    
    return jsonify({
        "query": query,
        "results": products,
        "count": len(products)
    }), 200

@app.route("/products/filter", methods=["GET"])
@handle_errors
def filter_products_endpoint():
    """Filter products by various criteria."""
    category = request.args.get('category')
    store = request.args.get('store')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    min_rating = request.args.get('min_rating', type=float)
    availability = request.args.get('availability')
    
    products = filter_products(
        category=category,
        min_price=min_price,
        max_price=max_price,
        store=store,
        min_rating=min_rating,
        availability=availability
    )
    
    return jsonify({
        "filters": {
            "category": category,
            "store": store,
            "price_range": [min_price, max_price],
            "min_rating": min_rating,
            "availability": availability
        },
        "results": products,
        "count": len(products)
    }), 200

@app.route("/products/compare", methods=["GET"])
@handle_errors
def compare_products():
    """Compare multiple products by IDs."""
    ids_param = request.args.get('ids', '')
    
    if not ids_param:
        return jsonify({"error": "No product IDs provided"}), 400
    
    try:
        product_ids = [int(id.strip()) for id in ids_param.split(',')]
    except ValueError:
        return jsonify({"error": "Invalid product IDs"}), 400
    
    if len(product_ids) < 2:
        return jsonify({"error": "At least 2 products required for comparison"}), 400
    
    if len(product_ids) > 10:
        return jsonify({"error": "Maximum 10 products can be compared"}), 400
    
    products = get_products_by_ids(product_ids)
    
    if not products:
        return jsonify({"error": "Products not found"}), 404
    
    return jsonify({
        "comparison": products,
        "count": len(products)
    }), 200

# ==================== STORES ENDPOINTS ====================

@app.route("/stores", methods=["GET"])
@handle_errors
def get_stores():
    """Get all available stores."""
    stores = get_all_stores()
    return jsonify({
        "stores": stores,
        "count": len(stores)
    }), 200

@app.route("/stores/<store_name>/products", methods=["GET"])
@handle_errors
@validate_pagination
def get_store_products(store_name, limit, offset):
    """Get all products from a specific store."""
    products = get_products_by_store(store_name)
    paginated = products[offset:offset+limit]
    
    return jsonify({
        "store": store_name,
        "data": paginated,
        "pagination": {
            "limit": limit,
            "offset": offset,
            "total": len(products)
        }
    }), 200

# ==================== CATEGORIES ENDPOINTS ====================

@app.route("/categories", methods=["GET"])
@handle_errors
def get_categories():
    """Get all available categories."""
    categories = get_all_categories()
    return jsonify({
        "categories": categories,
        "count": len(categories)
    }), 200

@app.route("/categories/<category_name>/products", methods=["GET"])
@handle_errors
@validate_pagination
def get_category_products(category_name, limit, offset):
    """Get all products in a specific category."""
    products = get_products_by_category(category_name)
    paginated = products[offset:offset+limit]
    
    return jsonify({
        "category": category_name,
        "data": paginated,
        "pagination": {
            "limit": limit,
            "offset": offset,
            "total": len(products)
        }
    }), 200

# ==================== PRICE COMPARISON ENDPOINTS ====================

@app.route("/price-comparison", methods=["GET"])
@handle_errors
def price_comparison():
    """Get price comparison for a product across stores."""
    product_name = request.args.get('product', '').strip()
    
    if not product_name:
        return jsonify({"error": "Product name required"}), 400
    
    comparison = get_price_comparison(product_name)
    
    if not comparison:
        return jsonify({"error": "No products found"}), 404
    
    return jsonify({
        "product": product_name,
        "comparison": comparison,
        "count": len(comparison),
        "cheapest": comparison[0] if comparison else None
    }), 200

# ==================== STATISTICS ENDPOINTS ====================

@app.route("/statistics", methods=["GET"])
@handle_errors
def statistics():
    """Get database statistics."""
    stats = get_statistics()
    return jsonify(stats), 200

# ==================== ADMIN ENDPOINTS ====================

@app.route("/admin/products", methods=["POST"])
@handle_errors
def create_product():
    """Create a new product (admin endpoint)."""
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['name', 'price', 'store', 'link', 'category']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400
    
    product_id = insert_product(
        name=data['name'],
        price=data['price'],
        store=data['store'],
        link=data['link'],
        image=data.get('image', ''),
        category=data.get('category', 'Electronics'),
        description=data.get('description', ''),
        original_price=data.get('original_price'),
        rating=data.get('rating', 0),
        availability=data.get('availability', 'in_stock')
    )
    
    if not product_id:
        return jsonify({"error": "Product already exists"}), 409
    
    return jsonify({
        "message": "Product created successfully",
        "product_id": product_id
    }), 201

@app.route("/admin/products/<int:product_id>", methods=["PUT"])
@handle_errors
def update_product_endpoint(product_id):
    """Update a product (admin endpoint)."""
    product = get_product_by_id(product_id)
    
    if not product:
        return jsonify({"error": "Product not found"}), 404
    
    data = request.get_json()
    success = update_product(product_id, **data)
    
    if not success:
        return jsonify({"error": "Failed to update product"}), 400
    
    return jsonify({
        "message": "Product updated successfully",
        "product_id": product_id
    }), 200

@app.route("/admin/products/<int:product_id>", methods=["DELETE"])
@handle_errors
def delete_product_endpoint(product_id):
    """Delete a product (admin endpoint)."""
    product = get_product_by_id(product_id)
    
    if not product:
        return jsonify({"error": "Product not found"}), 404
    
    success = delete_product(product_id)
    
    if not success:
        return jsonify({"error": "Failed to delete product"}), 400
    
    return jsonify({"message": "Product deleted successfully"}), 200

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({"error": "Internal server error"}), 500

# ==================== MAIN ====================

if __name__ == "__main__":
    logger.info("Starting PriceCompare API server...")
    app.run(host="0.0.0.0", port=5000, debug=True)
