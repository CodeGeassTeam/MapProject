from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username =  db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def get_json(self):
        return{
            'id': self.id,
            'username': self.username
        }

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

# class Admin(db.Model):
#     __tablename__ = 'admins'

#     id = db.Column(db.Integer, primary_key=True)
#     username =  db.Column(db.String(20), nullable=False, unique=True)
#     password = db.Column(db.String(120), nullable=False)

#     def __init__(self, username, password):
#         self.username = username
#         self.set_password(password)

#     def get_json(self):
#         return{
#             'id': self.id,
#             'username': self.username
#         }

#     def set_password(self, password):
#         """Create hashed password."""
#         self.password = generate_password_hash(password)
    
#     def check_password(self, password):
#         """Check hashed password."""
#         return check_password_hash(self.password, password)

#     # def addMarker(self, markerdetails):
#     #     new_todo = Todo(text=text)
#     #     new_todo.user_id = self.id
#     #     self.todos.append(new_todo)
#     #     db.session.add(self)
#     #     db.session.commit()
#     #     return new_marker

# #consider string for ids?


# class Location(db.Model):
#     __tablename__ = 'locations'

#     id = db.Column(db.Integer, primary_key=True)
#     latitude = db.Column(db.Float, nullable=False)
#     longitude = db.Column(db.Float, nullable=False)

#     buildings = db.relationship('BuildingDetails', back_populates='location', cascade='all, delete-orphan')


# class BuildingDetails(db.Model):
#     __tablename__ = 'building_details'

#     id = db.Column(db.Integer, primary_key=True)
#     location_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=False)
#     num_floors = db.Column(db.Integer, nullable=False)

#     location = db.relationship('Location', back_populates='buildings')
#     rooms = db.relationship('Room', back_populates='building', cascade='all, delete-orphan')


# class Room(db.Model):
#     __tablename__ = 'rooms'

#     id = db.Column(db.Integer, primary_key=True)
#     building_id = db.Column(db.Integer, db.ForeignKey('building_details.id'), nullable=False)
#     floor = db.Column(db.Integer, nullable=False)
#     room_number = db.Column(db.String(50), nullable=False)
#     room_name = db.Column(db.String(100), nullable=True)
#     faculty = db.Column(db.String(100), nullable=True)

#     building = db.relationship('BuildingDetails', back_populates='rooms')


class Marker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lat = db.Column(db.Float, nullable=False)
    lon = db.Column(db.Float, nullable=False)
    faculty = db.Column(db.String(100))
    building = db.Column(db.String(100), nullable=False)
    room = db.Column(db.String(100), nullable=False)
    floor = db.Column(db.String(100))
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    def __init__(self, lat, lon,faculty, building, room, floor):
        self.lat = lat
        self.lon = lon
        self.faculty = faculty
        self.building = building
        self.room = room
        self.floor = floor
#         self.user_id = user_id

    def get_json(self):
        return {
            'id': self.id,
            'lat': self.lat,
            'lon': self.lon,
            'faculty': self.faculty,
            'building': self.building,
            'room': self.room,
            'floor': self.floor,
#             'user_id': self.user_id
        }   
    
    def add_marker(self, lat, lon, faculty, building, room, floor):
        new_marker = Marker(lat=lat, lon=lon, faculty=faculty, building=building, room=room, floor=floor)
        db.session.add(new_marker)
        db.session.commit()
        return new_marker
    
    def get_all_markers(self):
        return Marker.query.all()
    
    def delete_marker(self, id):
        marker = Marker.query.get(id)
        if marker:
            db.session.delete(marker)
            db.session.commit()
            return True
        return False
    
    def update_marker(self, id, lat, lon, faculty, building, room, floor):
        marker = Marker.query.get(id)
        if marker:
            marker.lat = lat
            marker.lon = lon
            marker.faculty = faculty
            marker.building = building
            marker.room = room
            marker.floor = floor
            db.session.commit()
            return True
        return False