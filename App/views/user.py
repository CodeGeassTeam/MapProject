from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from App.models import *

from.index import index_views

from App.controllers import (
    create_user,
    get_all_users,
    get_all_users_json,
    jwt_required,
    create_marker
)

user_views = Blueprint('user_views', __name__, template_folder='../templates')

@user_views.route('/users', methods=['GET'])
def get_user_page():
    users = get_all_users()
    return render_template('users.html', users=users)

@user_views.route('/users', methods=['POST'])
def create_user_action():
    data = request.form
    flash(f"User {data['username']} created!")
    create_user(data['username'], data['password'])
    return redirect(url_for('user_views.get_user_page'))

@user_views.route('/api/users', methods=['GET'])
def get_users_action():
    users = get_all_users_json()
    return jsonify(users)

@user_views.route('/api/users', methods=['POST'])
def create_user_endpoint():
    data = request.json
    user = create_user(data['username'], data['password'])
    return jsonify({'message': f"user {user.username} created with id {user.id}"})

@user_views.route('/static/users', methods=['GET'])
def static_user_page():
  return send_from_directory('static', 'static-user.html')

@user_views.route('/admin/add', methods=['POST'])
@jwt_required()
def add_marker():
    data = request.json
    if not data:
        return jsonify({'message': 'No data provided'})

    try:
        new_marker = create_marker(
            lat=data['lat'],
            lon=data['lon'],
            faculty=data['faculty'],
            building=data['building'],
            room=data['room'],
            floor=data['floor'],
            user_id=jwt_current_user.id
        )
        return jsonify({'message': 'Marker added successfully', 'marker': new_marker})
    except Exception as e:
        return jsonify({'message': 'Failed to add marker'})
    
@user_views.route('/admin', methods=['GET'])
@jwt_required()
def admin_page():
    markers = Marker.query.all()  # Get all markers from database
    return render_template('admin.html')#, markers=markers)
