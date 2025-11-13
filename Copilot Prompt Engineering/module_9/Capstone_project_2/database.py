"""
Database handler for E-commerce application
"""
import sqlite3
import os

class DatabaseManager:
    def __init__(self, db_name="ecommerce.db"):
        self.db_name = db_name
        self.init_database()
    
    def init_database(self):
        """Initialize database with required tables"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Products table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                description TEXT,
                stock INTEGER DEFAULT 0
            )
        ''')
        
        # Cart table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cart (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER,
                quantity INTEGER,
                FOREIGN KEY (product_id) REFERENCES products (id)
            )
        ''')
        
        # Insert sample data if products table is empty
        cursor.execute("SELECT COUNT(*) FROM products")
        if cursor.fetchone()[0] == 0:
            sample_products = [
                ("Laptop", 999.99, "High-performance laptop", 10),
                ("Smartphone", 599.99, "Latest smartphone", 15),
                ("Headphones", 99.99, "Wireless headphones", 20),
                ("Tablet", 299.99, "10-inch tablet", 8)
            ]
            cursor.executemany(
                "INSERT INTO products (name, price, description, stock) VALUES (?, ?, ?, ?)",
                sample_products
            )
        
        conn.commit()
        conn.close()
    
    def get_connection(self):
        """Get database connection"""
        return sqlite3.connect(self.db_name)
    
    def get_all_products(self):
        """Get all products from database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # BUG 1: SQL injection vulnerability - using string formatting instead of parameterized queries
        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()
        conn.close()
        return products
    
    def get_product_by_id(self, product_id):
        """Get product by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # BUG 2: Not using parameterized query properly
        query = f"SELECT * FROM products WHERE id = {product_id}"
        cursor.execute(query)
        product = cursor.fetchone()
        conn.close()
        return product
    
    def add_to_cart(self, product_id, quantity):
        """Add product to cart"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Check if product exists and has enough stock
        product = self.get_product_by_id(product_id)
        if not product:
            return False
        
        # BUG 3: Not checking stock availability properly
        if product[4] < quantity:
            return False
        
        # Check if item already in cart
        cursor.execute("SELECT * FROM cart WHERE product_id = ?", (product_id,))
        existing_item = cursor.fetchone()
        
        if existing_item:
            # Update quantity
            new_quantity = existing_item[2] + quantity
            cursor.execute("UPDATE cart SET quantity = ? WHERE product_id = ?", 
                         (new_quantity, product_id))
        else:
            # Add new item
            cursor.execute("INSERT INTO cart (product_id, quantity) VALUES (?, ?)", 
                         (product_id, quantity))
        
        conn.commit()
        conn.close()
        return True
    
    def get_cart_items(self):
        """Get all cart items with product details"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT c.id, p.name, p.price, c.quantity, p.description
            FROM cart c
            JOIN products p ON c.product_id = p.id
        ''')
        
        cart_items = cursor.fetchall()
        conn.close()
        return cart_items
    
    def clear_cart(self):
        """Clear all items from cart"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cart")
        conn.commit()
        conn.close()
    
    def add_product(self, name, price, description, stock):
        """Add new product to database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # BUG 4: Missing input validation
        cursor.execute(
            "INSERT INTO products (name, price, description, stock) VALUES (?, ?, ?, ?)",
            (name, price, description, stock)
        )
        
        conn.commit()
        conn.close()
        return True
