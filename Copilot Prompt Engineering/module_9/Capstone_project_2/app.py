"""
E-commerce Web Application using Streamlit
"""
import streamlit as st
import pandas as pd
from product_manager import ProductManager

class EcommerceApp:
    def __init__(self):
        self.product_manager = ProductManager()
        
    def run(self):
        """Main application runner"""
        st.set_page_config(
            page_title="E-commerce Store", 
            page_icon="🛒",
            layout="wide"
        )
        
        # Custom CSS for better styling
        st.markdown("""
        <style>
        .main-header {
            font-size: 3rem;
            color: #1E88E5;
            text-align: center;
            margin-bottom: 2rem;
        }
        .product-card {
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 1rem;
            margin: 1rem 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .price {
            font-size: 1.5rem;
            font-weight: bold;
            color: #2E7D32;
        }
        .stock {
            color: #F57C00;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Header
        st.markdown('<h1 class="main-header">🛒 E-commerce Store</h1>', unsafe_allow_html=True)
        
        # Sidebar navigation
        page = st.sidebar.selectbox("Navigate", 
                                   ["Products", "Cart", "Admin Panel"])
        
        if page == "Products":
            self.show_products_page()
        elif page == "Cart":
            self.show_cart_page()
        else:
            self.show_admin_page()
    
    def show_products_page(self):
        """Display products page"""
        st.header("Products")
        
        # Search functionality
        col1, col2 = st.columns([3, 1])
        with col1:
            search_term = st.text_input("Search products", placeholder="Enter product name...")
        with col2:
            # BUG 15: Search button doesn't actually trigger search
            search_button = st.button("Search")
        
        # Get products
        if search_term:
            products = self.product_manager.search_products(search_term)
        else:
            products = self.product_manager.get_all_products()
        
        if not products:
            st.warning("No products found!")
            return
        
        # Display products
        for i in range(0, len(products), 2):
            cols = st.columns(2)
            
            for j, col in enumerate(cols):
                if i + j < len(products):
                    product = products[i + j]
                    
                    with col:
                        # BUG 16: Not handling empty or None descriptions
                        st.markdown(f"""
                        <div class="product-card">
                            <h3>{product['name']}</h3>
                            <p class="price">${product['price']:.2f}</p>
                            <p>{product['description']}</p>
                            <p class="stock">Stock: {product['stock']} items</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Add to cart section
                        quantity = st.number_input(
                            f"Quantity for {product['name']}", 
                            min_value=1, 
                            # BUG 17: Max value allows more than available stock
                            max_value=100,  
                            value=1,
                            key=f"qty_{product['id']}"
                        )
                        
                        if st.button(f"Add to Cart", key=f"add_{product['id']}"):
                            success, message = self.product_manager.add_product_to_cart(
                                product['id'], quantity
                            )
                            
                            if success:
                                st.success(message)
                            else:
                                st.error(message)
        
    def show_cart_page(self):
        """Display cart page"""
        st.header("Shopping Cart")
        
        cart_summary = self.product_manager.get_cart_summary()
        
        if not cart_summary['items']:
            st.info("Your cart is empty!")
            return
        
        # Display cart items
        cart_data = []
        for item in cart_summary['items']:
            cart_data.append({
                'Product': item['name'],
                'Price': f"${item['price']:.2f}",
                'Quantity': item['quantity'],
                'Subtotal': f"${item['subtotal']:.2f}"
            })
        
        # BUG 18: Not displaying tax information properly
        df = pd.DataFrame(cart_data)
        st.dataframe(df, use_container_width=True)
        
        # Cart summary
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Items", cart_summary['item_count'])
        with col2:
            # BUG 19: Showing subtotal as final total
            st.metric("Total Amount", f"${cart_summary['total']:.2f}")
        with col3:
            if st.button("Proceed to Checkout", type="primary"):
                self.process_checkout()
        
        # Clear cart option
        if st.button("Clear Cart"):
            self.product_manager.db.clear_cart()
            st.success("Cart cleared!")
            st.rerun()
    
    def process_checkout(self):
        """Process the checkout"""
        success, result = self.product_manager.process_checkout()
        
        if success:
            st.success("Order processed successfully!")
            
            # Display order summary
            st.subheader("Order Summary")
            
            order_data = []
            for item in result['items']:
                order_data.append({
                    'Product': item['name'],
                    'Price': f"${item['price']:.2f}",
                    'Quantity': item['quantity'],
                    'Subtotal': f"${item['subtotal']:.2f}"
                })
            
            df = pd.DataFrame(order_data)
            st.dataframe(df)
            
            # BUG 20: Order summary calculation display issues
            st.write(f"**Subtotal:** ${result['subtotal']:.2f}")
            st.write(f"**Tax:** ${result['tax']:.2f}")  
            st.write(f"**Total:** ${result['total']:.2f}")
            
        else:
            st.error(result)
    
    def show_admin_page(self):
        """Display admin panel"""
        st.header("Admin Panel")
        
        tab1, tab2, tab3 = st.tabs(["Add Product", "Inventory", "Low Stock Alert"])
        
        with tab1:
            st.subheader("Add New Product")
            
            with st.form("add_product_form"):
                name = st.text_input("Product Name")
                price = st.number_input("Price", min_value=0.01, step=0.01)
                description = st.text_area("Description")
                stock = st.number_input("Stock Quantity", min_value=0, step=1)
                
                submitted = st.form_submit_button("Add Product")
                
                if submitted:
                    # BUG 21: Not validating form inputs properly
                    success, message = self.product_manager.add_new_product(
                        name, price, description, stock
                    )
                    
                    if success:
                        st.success(message)
                    else:
                        st.error(message)
        
        with tab2:
            st.subheader("Current Inventory")
            
            products = self.product_manager.get_all_products()
            
            if products:
                inventory_data = []
                for product in products:
                    inventory_data.append({
                        'ID': product['id'],
                        'Name': product['name'],
                        'Price': f"${product['price']:.2f}",
                        'Stock': product['stock'],
                        'Description': product['description'][:50] + "..." if len(product['description']) > 50 else product['description']
                    })
                
                df = pd.DataFrame(inventory_data)
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No products in inventory")
        
        with tab3:
            st.subheader("Low Stock Alert")
            
            threshold = st.number_input("Stock Threshold", min_value=1, value=5)
            
            # BUG 22: Low stock function has logic error (from ProductManager)
            low_stock_products = self.product_manager.get_low_stock_products(threshold)
            
            if low_stock_products:
                st.warning(f"Found {len(low_stock_products)} products with low stock!")
                
                low_stock_data = []
                for product in low_stock_products:
                    low_stock_data.append({
                        'Name': product['name'],
                        'Current Stock': product['stock'],
                        'Price': f"${product['price']:.2f}"
                    })
                
                df = pd.DataFrame(low_stock_data)
                st.dataframe(df)
            else:
                st.success("All products have sufficient stock!")

if __name__ == "__main__":
    app = EcommerceApp()
    app.run()
