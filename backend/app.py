from flask import Flask, jsonify
from flask_cors import CORS
from database import get_all_products

app = Flask(__name__)
CORS(app)  # 👈 this line allows frontend requests

@app.route("/products")
def products():
    return jsonify(get_all_products())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
