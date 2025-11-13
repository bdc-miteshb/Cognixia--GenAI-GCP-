"""
Product Manager for E-commerce application
Handles business logic for products and cart operations
"""
from database import DatabaseManager

class ProductManager:
    def __init__(self):
        self.db = DatabaseManager()
    
    def get_all_products(self):
        """Get all products with formatted data"""
        products = self.db.get_all_products()
        formatted_products = []
        
        for product in products:
            formatted_product = {
                'id': product[0],
                'name': product[1],
                'price': product[2],
                'description': product[3],
                'stock': product[4]
            }
            formatted_products.append(formatted_product)
        
        return formatted_products
    
    def get_product_details(self, product_id):
        """Get detailed product information"""
        try:
            product = self.db.get_product_by_id(product_id)
            if product:
                return {
                    'id': product[0],
                    'name': product[1],
                    'price': product[2],
                    'description': product[3],
                    'stock': product[4]
                }
            return None
        except Exception as e:
            # BUG 5: Poor error handling - not logging or properly handling errors
            return None
    
    def add_product_to_cart(self, product_id, quantity):
        """Add product to cart with validation"""
        try:
            # BUG 6: Not validating quantity is positive
            if quantity <= 0:
                return False, "Invalid quantity"
            
            product = self.get_product_details(product_id)
            if not product:
                return False, "Product not found"
            
            # BUG 7: Logic error in stock checking
            if product['stock'] < quantity:
                return False, f"Only {product['stock']} items available"
            
            success = self.db.add_to_cart(product_id, quantity)
            if success:
                return True, "Product added to cart successfully"
            else:
                return False, "Failed to add product to cart"
                
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def get_cart_summary(self):
        """Get cart items with total calculation"""
        cart_items = self.db.get_cart_items()
        cart_data = []
        total_amount = 0
        
        for item in cart_items:
            item_data = {
                'id': item[0],
                'name': item[1],
                'price': item[2],
                'quantity': item[3],
                'description': item[4],
                'subtotal': item[2] * item[3]
            }
            cart_data.append(item_data)
            
            # BUG 8: Calculation error - not adding tax
            total_amount += item[2] * item[3]
        
        return {
            'items': cart_data,
            'total': total_amount,
            'item_count': len(cart_data)
        }
    
    def calculate_total_with_tax(self, subtotal):
        """Calculate total amount including tax"""
        # BUG 9: Hard-coded tax rate without configuration
        tax_rate = 0.08  # 8% tax
        tax_amount = subtotal * tax_rate
        return subtotal + tax_amount
    
    def process_checkout(self):
        """Process checkout and return order summary"""
        cart_summary = self.get_cart_summary()
        
        if not cart_summary['items']:
            return False, "Cart is empty"
        
        # BUG 10: Not updating stock after checkout
        subtotal = cart_summary['total']
        total_with_tax = self.calculate_total_with_tax(subtotal)
        
        # Clear cart after checkout
        self.db.clear_cart()
        
        order_summary = {
            'items': cart_summary['items'],
            'subtotal': subtotal,
            'tax': total_with_tax - subtotal,
            'total': total_with_tax,
            'item_count': cart_summary['item_count']
        }
        
        return True, order_summary
    
    def add_new_product(self, name, price, description, stock):
        """Add new product with validation"""
        # BUG 11: Insufficient input validation
        if not name or not price:
            return False, "Name and price are required"
        
        try:
            # BUG 12: Not checking if price is negative
            price = float(price)
            stock = int(stock)
            
            success = self.db.add_product(name, price, description, stock)
            if success:
                return True, "Product added successfully"
            else:
                return False, "Failed to add product"
                
        except ValueError:
            return False, "Invalid price or stock value"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def search_products(self, search_term):
        """Search products by name"""
        all_products = self.get_all_products()
        
        if not search_term:
            return all_products
        
        # BUG 13: Case-sensitive search
        filtered_products = []
        for product in all_products:
            if search_term in product['name']:
                filtered_products.append(product)
        
        return filtered_products
    
    def get_low_stock_products(self, threshold=5):
        """Get products with low stock"""
        all_products = self.get_all_products()
        low_stock_products = []
        
        for product in all_products:
            # BUG 14: Using >= instead of <=
            if product['stock'] >= threshold:
                low_stock_products.append(product)
        
        return low_stock_products
