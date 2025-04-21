from .user import create_user, create_marker
from App.database import db
from App.models import *

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