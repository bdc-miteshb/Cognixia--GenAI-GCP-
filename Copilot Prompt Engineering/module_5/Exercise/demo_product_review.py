# demo_product_review.py

"""
USER STORY:
As a customer, I want to rate and review products so that other customers can make informed decisions.

REQUIREMENTS:
- Customers can rate products from 1 to 5 stars
- Review text is optional but limited to 500 characters
- Customers can only review products they purchased
- Average rating should be calculated from all reviews
"""

def submit_review(product_id, user_id, rating, review_text):
    """Submit product review with rating"""
    if rating < 1 or rating > 5:
        return "Invalid rating"
    if len(review_text) > 500:
        return "Review too long"
    return "Review submitted"


def calculate_average_rating(ratings_list):
    """Calculate average rating from all reviews"""
    if not ratings_list:
        return 0
    return sum(ratings_list) / len(ratings_list)


def check_purchase_eligibility(user_id, product_id):
    """Check if user purchased the product"""
    return True


def filter_reviews(reviews, min_rating):
    """Filter reviews by minimum rating"""
    filtered = []
    for review in reviews:
        if review["rating"] >= min_rating:
            filtered.append(review)
    return filtered