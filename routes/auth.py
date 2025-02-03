from flask import Blueprint, jsonify, request, session
from werkzeug.security import check_password_hash

from forms import RegistrationForm, LoginForm
from models import User
from extensions import db

auth_bp = Blueprint('auth', __name__)

# Register an user
@auth_bp.route('/register', methods=['POST'])
def register():
    form = RegistrationForm(data=request.json)
    
    if form.validate_on_submit():
        # Email checking
        if User.query.filter_by(email=form.email.data).first():
            return jsonify({
                'success': False,
                'message': 'Email already registered'
            }), 400
        
        user = User(username = form.username.data, email = form.email.data)
        user.set_password(form.password.data)
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': {'user_id': user.id},
            'message': 'User registered successfully!'
        }), 201
    
    return jsonify({
        'success': False,
        'errors': form.errors
        }), 400
    
# User login
@auth_bp.route('/login', methods=['POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # User search by username/email
        user = User.query.filter((User.username == form.who.data) | (User.email == form.who.data)).first()
        
        if user and check_password_hash(user.hash_password, form.password.data):
            # Log in
            session['user_id'] = user.id
            return jsonify({
                'success': True,
                'data': {'user_id': user.id},
                'message': 'You has been logged in!'
        }), 200
            
    return jsonify({
        'success': False,
        'message': 'Incorrect login or password'
    }), 400
    
# User logout
@auth_bp.route('/logout', methods=['POST'])
def logout():
    if 'user_id' in session:
        session.pop('user_id', None)
        return jsonify({
            'success': True,
            'message': 'You have logged out'
        }), 200
    return jsonify({
            'success': False,
            'message': 'You have not logged out'
    }), 200