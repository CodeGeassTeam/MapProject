from .user import create_user, create_marker
from App.database import db


def initialize():
    db.drop_all()
    db.create_all()
    create_user('bob', 'bobpass')
    create_marker('10.641442', '-61.400783', 'Science & Technology', 'Natural Sciences Building', 'CSL1', '3rd Floor')
    create_marker('10.639489', '-61.399761', 'Engineering', 'Chemical Engineering Max Richard Building', 'LT1', '1st Floor')
    create_marker('10.642012', '-61.400740', 'Law', 'Law and SALISES Building', 'Lecture Theater', '1st Floor')
