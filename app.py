import sqlite3
import streamlit as st

# Function to fetch products
def fetch_products():
    conn = sqlite3.connect('ecommerce_db.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, description, price, image_url, product_url FROM products")
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    return products

# Streamlit app
def main():
    st.title("Product Carousel")

    # Fetch products from the database
    products = fetch_products()

    # Display products
    for product in products:
        st.markdown(f"### {product[1]}")
        st.markdown(f"**Description:** {product[2]}")
        st.markdown(f"**Price:** ${product[3]}")
        st.image(product[4], width=200)
        st.markdown(f"[View Product]({product[5]})")

if __name__ == '__main__':
    main()
