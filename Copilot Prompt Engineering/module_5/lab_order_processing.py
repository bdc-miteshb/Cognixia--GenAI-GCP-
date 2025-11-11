# lab_order_processing.py

"""
USER STORY:
As a customer, I want to place and track orders so that I can receive my purchased items.

REQUIREMENTS:
- Customers can place orders with multiple items
- Order total must be greater than $10
- Free shipping for orders above $50
- Orders can be cancelled within 24 hours
- Order status: pending, confirmed, shipped, delivered, cancelled
"""

def create_order(customer_id, items, total_amount):
    """Create new order"""
    if total_amount < 10:
        return "Order minimum is $10"
    if not items:
        return "Order must have items"
    return {"order_id": "ORD123", "status": "pending"}


def calculate_shipping(total_amount):
    """Calculate shipping cost"""
    if total_amount >= 50:
        return 0
    return 5.99


def cancel_order(order_id, hours_since_order):
    """Cancel order if within 24 hours"""
    if hours_since_order > 24:
        return "Cannot cancel after 24 hours"
    return "Order cancelled"


def update_order_status(order_id, new_status):
    """Update order status"""
    valid_statuses = ["pending", "confirmed", "shipped", "delivered", "cancelled"]
    if new_status not in valid_statuses:
        return "Invalid status"
    return f"Status updated to {new_status}"


def apply_discount_code(total_amount, discount_code):
    """Apply discount code to order"""
    if discount_code == "SAVE10":
        return total_amount * 0.9
    elif discount_code == "SAVE20":
        return total_amount * 0.8
    return total_amount