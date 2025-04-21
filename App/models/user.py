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


class Location(db.Model):
    __tablename__ = 'locations'

    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    buildings = db.relationship('Building', back_populates='location', cascade='all, delete-orphan')

class Building(db.Model):
    __tablename__ = 'buildings'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    faculty = db.Column(db.String(100))
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=False)
    
    location = db.relationship('Location', back_populates='buildings')
    rooms = db.relationship('Room', back_populates='building', cascade='all, delete-orphan')

class Room(db.Model):
    __tablename__ = 'rooms'

    id = db.Column(db.Integer, primary_key=True)
    room_number = db.Column(db.String(100), nullable=False)
    floor = db.Column(db.Integer, nullable=False)
    building_id = db.Column(db.Integer, db.ForeignKey('buildings.id'))

    building = db.relationship('Building', back_populates='rooms')


class Marker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lat = db.Column(db.Float, nullable=False)
    lon = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(100), nullable=True)
    faculty = db.Column(db.String(100), nullable=True)
    building_id = db.Column(db.Integer, db.ForeignKey('buildings.id'), nullable=True)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'), nullable=True)

    building = db.relationship('Building', backref='markers')
    room = db.relationship('Room', backref='markers')

    def add_marker(self, lat, lon, faculty, building=None, room=None, image=None):
        new_marker = Marker(lat=lat, lon=lon, faculty=faculty, building=building, room=room, image=image)
        db.session.add(new_marker)
        db.session.commit()
        return new_marker

    def get_json(self):
        return {
            'id': self.id,
            'lat': self.lat,
            'lon': self.lon,
            'faculty': self.faculty,
            'building': self.building.name if self.building else None,
            'room': self.room.room_number if self.room else None,
            'image': self.image
        } 
    
    def add_marker(self, lat, lon, faculty, building=None, room=None, image=None):
        new_marker = Marker(lat=lat, lon=lon, faculty=faculty, building=building, room=room, image=image)
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
    
    def update_marker(self, id, lat=None, lon=None, faculty=None, building=None, room=None, image=None):
        marker = Marker.query.get(id)
        if marker:
            if lat is not None:
                marker.lat = lat
            if lon is not None:
                marker.lon = lon
            if faculty is not None:
                marker.faculty = faculty
            if building is not None:
                marker.building = building
            if room is not None:
                marker.room = room
            if image is not None:
                marker.image = image
            db.session.commit()
            return True
        return False