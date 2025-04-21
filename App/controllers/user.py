from App.models import User, Marker
from App.database import db

def create_user(username, password):
    newuser = User(username=username, password=password)
    db.session.add(newuser)
    db.session.commit()
    return newuser

def get_user_by_username(username):
    return User.query.filter_by(username=username).first()

def get_user(id):
    return User.query.get(id)

def get_all_users():
    return User.query.all()

def get_all_users_json():
    users = User.query.all()
    if not users:
        return []
    users = [user.get_json() for user in users]
    return users

def update_user(id, username):
    user = get_user(id)
    if user:
        user.username = username
        db.session.add(user)
        return db.session.commit()
    return None
    
def create_marker(lat, lon, faculty, building_name, room_number, floor):
    # Try to get the building from the DB (create if it doesn't exist)
    building = Building.query.filter_by(name=building_name).first()
    if not building:
        # Create a new building if it doesn't exist (you might also want to link a location here)
        building = Building(name=building_name, faculty=faculty, location_id=1)  # Make sure location_id=1 exists
        db.session.add(building)
        db.session.commit()

    # Try to get the room (create if it doesn't exist)
    room = Room.query.filter_by(room_number=room_number, floor=floor, building_id=building.id).first()
    if not room:
        room = Room(room_number=room_number, floor=floor, building=building)
        db.session.add(room)
        db.session.commit()

    # Now create the marker with actual Building and Room objects
    new_marker = Marker(
        lat=lat,
        lon=lon,
        faculty=faculty,
        building=building,
        room=room
    )
    db.session.add(new_marker)
    db.session.commit()
    return new_marker