import streamlit as st
import mysql.connector
import os
from PIL import Image
import requests
from io import BytesIO

# Function to fetch products
def fetch_products():
    conn = mysql.connector.connect(
        host=os.environ.get('DB_HOST', 'localhost'),
        user=os.environ.get('DB_USER', 'root'),
        password=os.environ.get('DB_PASSWORD', 'Singh@123'),
        database=os.environ.get('DB_NAME', 'ecommerce_db')
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, name, description, price, image_url, product_url FROM products")
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    return products

# Streamlit app
def main():
    st.title('E-commerce Products')

    products = fetch_products()

    # Display products
    for product in products:
        col1, col2 = st.columns([1, 3])

        with col1:
            try:
                response = requests.get(product['image_url'])
                img = Image.open(BytesIO(response.content))
                st.image(img, width=150)
            except Exception as e:
                st.error(f"Unable to load image: {e}")

        with col2:
            st.subheader(product['name'])
            st.write(product['description'])
            st.write(f"Price: ${product['price']:.2f}")
            if st.button('View Product', key=product['id']):
                st.markdown(f"[Go to product page]({product['product_url']})")

        st.markdown("---")

if __name__ == '__main__':
    main()
