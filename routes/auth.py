from flask import Blueprint, jsonify, request, session

from forms import RegistrationForm, LoginForm
from models import User

from extensions import db
from utils.auth_helper import check_access

auth_bp = Blueprint('auth', __name__)

# Register an user
@auth_bp.route('/register', methods = ['POST'])
def register():
    # Authorization check
    access = check_access(False)
    if access:
        return access
    
    # Initializing the form
    form = RegistrationForm(data = request.json)
    
    if form.validate_on_submit():
        # Username checking
        if User.query.filter_by(username = form.username.data).first():
            return jsonify({'error': 'Username already registered'}), 400
        
        # Email checking
        if User.query.filter_by(email = form.email.data).first():
            return jsonify({'error': 'Email already registered'}), 400
        
        # Initialize a new user with a hashed password
        user = User(username = form.username.data, email = form.email.data)
        user.set_password(form.password.data)
        
        # Added new user to the DB
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'message': 'User registered successfully!',
            'user_id': user.id
        }), 201
    
    return jsonify({'error': form.errors}), 400

# User login
@auth_bp.route('/login', methods = ['POST'])
def login():
    # Authorization check
    access = check_access(False)
    if access:
        return access
    
    # Initializing the form
    form = LoginForm(data = request.json)
    
    if form.validate_on_submit():
        # User search by username/email
        user = User.query.filter((User.username == form.who.data) | (User.email == form.who.data)).first()
        
        if user and user.check_password(form.password.data):
             # Adding an user to a session (login)
            session['user_id'] = user.id
            
            return jsonify({
                'message': 'You have been logged in!',
                'user_id': user.id
            }), 200
            
        return jsonify({'error': 'Incorrect login or password'}), 400
    
    return jsonify({'error': form.errors}), 400

# User logout
@auth_bp.route('/logout', methods = ['POST'])
def logout():
    # Authorization check
    access = check_access(True)
    if access:
        return access
    
    # Removing a user from a session (logging out)
    session.pop('user_id', None)
    
    return jsonify({'message': 'You have logged out'}), 200