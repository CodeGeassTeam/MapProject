from App.models import *
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

# def login_user(username, password):
#   user = User.query.filter_by(username=username).first()
#   if user and user.check_password(password):
#     token = create_access_token(identity=user)
#     return token
#   return None

def create_marker(lat, lon, faculty, building_name, room_number, floor):
    try:
        
        # Get or create building
        building = Building.query.filter_by(name=building_name).first()
        if not building:
            if not Location.query.first():
                raise ValueError("No locations exist in database!")
            building = Building(
                name=building_name, 
                faculty=faculty, 
                location_id=1  # Using first location
            )
            db.session.add(building)
            db.session.flush()  # Assigns ID without commit
        
        # Get or create room
        room = Room.query.filter_by(
            room_number=room_number, 
            floor=floor, 
            building_id=building.id
        ).first()
        
        if not room:
            room = Room(
                room_number=room_number,
                floor=floor,
                building_id=building.id
            )
            db.session.add(room)
            db.session.flush()
        
        # Create marker
        marker = Marker(
            lat=lat,
            lon=lon,
            faculty=faculty,
            building_id=building.id,
            room_id=room.id
        )
        db.session.add(marker)
        db.session.commit()
        return marker
        
    except Exception as e:
        db.session.rollback()
        print(f"Error creating marker: {str(e)}")
        raise