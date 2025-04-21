import os
from flask import Flask, render_template
from flask_uploads import DOCUMENTS, IMAGES, TEXT, UploadSet, configure_uploads
from flask_cors import CORS
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage


from App.database import init_db
from App.config import load_config

import os
from flask import Flask, request, render_template, flash, redirect, url_for, jsonify
from functools import wraps
from models import db, Admin, RegularUser, Todo, User

from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    get_jwt_identity,
    jwt_required,
    current_user,
    set_access_cookies,
    unset_jwt_cookies,
    current_user,
)

from App.controllers import (
    setup_jwt,
    add_auth_context
)

from App.views import views, setup_admin

def add_views(app):
    for view in views:
        app.register_blueprint(view)

def create_app(overrides={}):
    app = Flask(__name__, static_url_path='/static')
    app.config['TEMPLATES_AUTO_RELOAD'] = True  # Add this line
    load_config(app, overrides)
    CORS(app)
    add_auth_context(app)
    photos = UploadSet('photos', TEXT + DOCUMENTS + IMAGES)
    configure_uploads(app, photos)
    add_views(app)
    init_db(app)
    jwt = setup_jwt(app)
    setup_admin(app)
    @jwt.invalid_token_loader
    @jwt.unauthorized_loader
    def custom_unauthorized_response(error):
        return render_template('401.html', error=error), 401
    app.app_context().push()
    return app

app = create_app()
jwt = JWTManager(app)


@jwt.user_identity_loader
def user_identity_lookup(user):
  return user.id


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
  identity = jwt_data["sub"]
  return User.query.get(identity)

@jwt.expired_token_loader
@jwt.invalid_token_loader
def custom_unauthorized_response(error):
    return render_template('401.html', error=error), 401

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return render_template('401.html'), 401  

# custom decorator authorize routes for admin or regular user
def login_required(required_class):

  def wrapper(f):

    @wraps(f)
    @jwt_required()  # Ensure JWT authentication
    def decorated_function(*args, **kwargs):
      user = User.query.get(get_jwt_identity())
      if user.__class__ != required_class:  # Check class equality
        return jsonify(message='Invalid user role'), 403
      return f(*args, **kwargs)

    return decorated_function

  return wrapper


def login_user(username, password):
  user = User.query.filter_by(username=username).first()
  if user and user.check_password(password):
    token = create_access_token(identity=user)
    return token
  return None


# View Routes


@app.route('/', methods=['GET'])
def home_page():
  return render_template('home.html')


@app.route('/app', methods=['GET'])
@jwt_required()
def todos_page():
  return render_template('home.html', current_user=current_user)


@app.route('/login', methods=['GET'])
def login_page():
  return render_template('login.html')


@app.route('/admin', methods = ['GET'])
def admin_page():
   return render_template('admin.html')





@app.route('/login', methods=['POST'])
def login_action():
  data = request.form
  token = login_user(data['username'], data['password'])
  response = None
  user = User.query.filter_by(username=data['username']).first()
  if token:
    flash('Logged in successfully.')  # send message to next page
    response = redirect(url_for('admin_page'))  # redirect to main page if login successful
    set_access_cookies(response, token)
  else:
    flash('Invalid username or password')  # send message to next page
    response = redirect(url_for('login_page'))
  return response




@app.route('/createMarker', methods=['POST'])
@jwt_required()
def create_marker_action():
  data = request.form
  current_user.add_todo(data['text'])
  flash('Created')
  return redirect(url_for('admin_page'))



@app.route('/deleteMarker/<id>', methods=["GET"])
@jwt_required()
def delete_marker_action(id):
  res = current_user.delete_marker(id)
  if res == None:
    flash('Invalid id or unauthorized')
  else:
    flash('Marker Deleted')
  return redirect(url_for('home_page'))


@app.route('/editTodo/<id>', methods=["POST"])
@jwt_required()
def edit_Marker_action(id):
  data = request.form
  res = current_user.update_marker(id, data["text"])
  if res:
    flash('Marker Updated!')
  else:
    flash('Marker not found or unauthorized')
  return redirect(url_for('home_page'))










@app.route('/logout', methods=['GET'])
@jwt_required()
def logout_action():
  flash('Logged Out')
  response = redirect(url_for('login_page'))
  unset_jwt_cookies(response)
  return response






if __name__ == "__main__":
  app.run(host='0.0.0.0', port=81)
