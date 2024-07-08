from flask import Flask, render_template
import mysql.connector
import os

app = Flask(__name__)

# Function to fetch products
def fetch_products():
    conn = mysql.connector.connect(
        host=os.environ.get('DB_HOST'),
        user=os.environ.get('DB_USER'),
        password=os.environ.get('DB_PASSWORD'),
        database=os.environ.get('DB_NAME')
    )
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
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
