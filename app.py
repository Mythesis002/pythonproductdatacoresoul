from flask import Flask, render_template
import sqlite3
import os

app = Flask(__name__)

# Function to fetch products
def fetch_products():
    conn = sqlite3.connect('ecommerce_db.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, description, price, image_url, product_url FROM products")
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    return products

# Route for rendering index.html
@app.route('/')
def home():
    products = fetch_products()
    return render_template('index.html', products=products)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
