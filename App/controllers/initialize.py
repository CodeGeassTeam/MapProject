from .user import create_user, create_marker
from App.database import db
from App.models import *


# def initialize():
#     db.drop_all()
#     db.create_all()
#     create_user('bob', 'bobpass')
#     create_marker('10.641442', '-61.400783', 'Science & Technology', 'Natural Sciences Building', 'CSL1', '3rd Floor')
#     create_marker('10.639489', '-61.399761', 'Engineering', 'Chemical Engineering Max Richard Building', 'LT1', '1st Floor')
#     create_marker('10.642012', '-61.400740', 'Law', 'Law and SALISES Building', 'Lecture Theater', '1st Floor')

# def initialize():
#     print("Starting initialization...")
#     db.drop_all()
#     db.create_all()
#     print("Database tables created")
    
#     # Create and verify location
#     loc = Location(latitude=10.640559, longitude=-61.399576)
#     db.session.add(loc)
#     db.session.commit()
#     print(f"Location created with ID: {loc.id}")
    
#     # Verify location exists
#     print(f"Locations in DB: {Location.query.count()}")
    
#     # Create user
#     user = create_user('bob', 'bobpass')
#     print(f"User created: {user.username}")
#     print(f"Users in DB: {User.query.count()}")
    
#     # Create markers with verification
#     markers = [
#         (10.641442, -61.400783, 'Science', 'Natural Sciences', 'CSL1', '3rd'),
#         (10.639489, -61.399761, 'Engineering', 'Chemical Eng', 'LT1', '1st'),
#         (10.642012, -61.400740, 'Law', 'Law Building', 'LT1', '1st')
#     ]

#     create_markers = [
#         (lat, lon, faculty, building_name, room_number, floor) for lat, lon, faculty, building_name, room_number, floor in markers
#     ]


#     # for mark in markers:
#     #     marker = create_marker(mark[0], mark[1], mark[2], mark[3], mark[4], mark[5])
#     #     print(f"Created marker ID: {marker.id}")
    
#     print(f"Total markers: {Marker.query.count()}")
#     print(f"Total buildings: {Building.query.count()}")
#     print(f"Total rooms: {Room.query.count()}")
    
#     # Explicit final commit
#     db.session.commit()
#     print("Initialization complete")

def initialize():
    # Reset database
    db.drop_all()
    db.create_all()
    
    try:
        # Create initial location
        loc = Location(latitude=10.640559, longitude=-61.399576)
        db.session.add(loc)
        db.session.commit()
        
        # Create admin user
        user = create_user('bob', 'bobpass')
        
        # Create sample markers
        markers = [
            (10.641442, -61.400783, 'Science & Technology', 'Natural Sciences', 'CSL1', '3rd'),
            (10.639489, -61.399761, 'Engineering', 'Chemical Eng', 'LT1', '1st'),
            (10.642012, -61.400740, 'Law', 'Law Building', 'LT1', '1st')
        ]
        
        for coords in markers:
            create_marker(*coords)
        
        
    except Exception as e:
        db.session.rollback()
        print(f"Initialization failed: {str(e)}")
        raise