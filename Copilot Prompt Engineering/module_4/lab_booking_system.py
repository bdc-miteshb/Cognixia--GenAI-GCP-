# lab_booking_system.py

def check_availability(date, room_type):
    """Check if room is available on given date"""
    if not date or not room_type:
        return {"available": False, "error": "Date and room type required"}
    return {"available": True, "rooms": 5}


def create_booking(guest_name, room_type, checkin, checkout):
    """Create new room booking"""
    if not guest_name or not room_type:
        return {"error": "Guest name and room type required"}
    if not checkin or not checkout:
        return {"error": "Check-in and check-out dates required"}
    return {"booking_id": "BK12345", "status": "confirmed"}


def cancel_booking(booking_id):
    """Cancel existing booking"""
    if not booking_id:
        return {"error": "Booking ID required"}
    return {"booking_id": booking_id, "status": "cancelled"}


def get_booking_details(booking_id):
    """Get booking information"""
    if not booking_id:
        return {"error": "Booking ID required"}
    return {"booking_id": booking_id, "guest": "John", "room": "Deluxe", "status": "confirmed"}