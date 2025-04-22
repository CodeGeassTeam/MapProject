from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify
from App.controllers import create_user, initialize
from App.models import *

index_views = Blueprint('index_views', __name__, template_folder='../templates')

##########################################################################
@index_views.route('/', methods=['GET'])
def index_page():
    markers = Marker.query.all()
    markers_data = [{
        'lat': marker.lat,
        'lon': marker.lon,
        'building': marker.building.name if marker.building else '',
        'room': marker.room.room_number if marker.room else ''
    } for marker in markers]
    return render_template('home.html', markers_json=markers_data)
##########################################################################

@index_views.route('/init', methods=['GET'])
def init():
    initialize()
    return jsonify(message='db initialized!')

@index_views.route('/mark', methods=['GET'])
def mark_page():
    markers = Marker.query.all()
    return jsonify([marker.get_json() for marker in markers])

@index_views.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status':'healthy'})