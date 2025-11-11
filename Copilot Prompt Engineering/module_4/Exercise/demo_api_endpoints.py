# demo_api_endpoints.py

def get_user(user_id):
    """GET /api/users/{id} - Retrieve user by ID"""
    if not user_id:
        return {"error": "User ID required"}
    return {"id": user_id, "name": "John", "status": "active"}


def create_user(name, email):
    """POST /api/users - Create new user"""
    if not name or not email:
        return {"error": "Name and email required"}
    return {"id": 123, "name": name, "email": email, "status": "created"}


def update_user(user_id, data):
    """PUT /api/users/{id} - Update user details"""
    if not user_id:
        return {"error": "User ID required"}
    return {"id": user_id, "updated": True}


def delete_user(user_id):
    """DELETE /api/users/{id} - Delete user"""
    if not user_id:
        return {"error": "User ID required"}
    return {"id": user_id, "deleted": True}