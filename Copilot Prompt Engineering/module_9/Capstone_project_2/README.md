# E-commerce Web Application

## Project Overview
A simple e-commerce web application built with Python, Streamlit, and SQLite. This application allows users to browse products, add items to cart, and process checkout with a clean, professional interface.

## Features
- **Product Catalog**: Browse and search through available products
- **Shopping Cart**: Add products to cart with quantity selection
- **Checkout Process**: Calculate totals with tax and process orders
- **Admin Panel**: Add new products and manage inventory
- **Low Stock Alerts**: Monitor products with low inventory levels

## Project Structure
```
ecommerce-app/
├── app.py                 # Main Streamlit application (Frontend)
├── product_manager.py     # Business logic and product operations (Backend)
├── database.py           # Database operations and management (Backend)
├── README.md            # Project documentation
└── ecommerce.db         # SQLite database (auto-generated)
```

## Technology Stack
- **Frontend**: Streamlit
- **Backend**: Python with class-based architecture
- **Database**: SQLite
- **Styling**: Custom CSS for professional appearance

## Installation & Setup

### Prerequisites
- Python 3.7+
- pip package manager

### Required Packages
```bash
pip install streamlit pandas
```

### Running the Application
1. Clone or download the project files
2. Navigate to the project directory
3. Run the Streamlit application:
```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

## Application Usage

### Customer Features
1. **Browse Products**: View all available products with details and pricing
2. **Search Products**: Use the search bar to find specific items
3. **Add to Cart**: Select quantity and add products to shopping cart
4. **View Cart**: Review selected items and quantities
5. **Checkout**: Complete purchase with automatic tax calculation

### Admin Features
1. **Add Products**: Add new products to the catalog with name, price, description, and stock
2. **View Inventory**: Monitor current stock levels and product information
3. **Low Stock Alerts**: Set threshold levels to identify products needing restocking

## Database Schema

### Products Table
- `id`: Primary key (auto-increment)
- `name`: Product name (text)
- `price`: Product price (decimal)
- `description`: Product description (text)
- `stock`: Available quantity (integer)

### Cart Table
- `id`: Primary key (auto-increment)
- `product_id`: Foreign key referencing products table
- `quantity`: Number of items in cart (integer)

## Key Components

### DatabaseManager Class
- Handles all database operations
- Manages SQLite connections
- Provides CRUD operations for products and cart

### ProductManager Class
- Contains business logic for product operations
- Handles cart management and calculations
- Processes checkout and order management
- Manages product search and inventory tracking

### EcommerceApp Class
- Main Streamlit application class
- Manages UI components and user interactions
- Coordinates between frontend and backend components
- Handles page navigation and display logic

## Configuration
- **Tax Rate**: Currently set to 8% (configurable in ProductManager class)
- **Database**: SQLite database file created automatically
- **Sample Data**: Application includes sample products for testing

## Sample Products
The application comes pre-loaded with sample products:
- Laptop ($999.99)
- Smartphone ($599.99)
- Headphones ($99.99)
- Tablet ($299.99)

## Development Notes
- All backend logic is separated from frontend components
- Class-based architecture for maintainability
- Professional styling with custom CSS
- Error handling for database operations
- Input validation for user inputs

## Future Enhancements
- User authentication and accounts
- Order history tracking
- Payment gateway integration
- Product categories and filtering
- Inventory management notifications
- Product image support

## Troubleshooting
- If the application doesn't start, ensure all required packages are installed
- For database issues, delete the `ecommerce.db` file and restart the application
- Check console output for detailed error messages

## License
This project is created for educational purposes as part of a capstone project.
