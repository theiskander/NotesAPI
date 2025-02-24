from flask import Blueprint, jsonify, request

from forms import RegistrationForm
from models import User
from extensions import db

auth_bp = Blueprint('auth', __name__)

# Register an user
@auth_bp.route('/register', methods=['POST'])
def register():
    # Initializing the form
    form = RegistrationForm(data=request.json)
    
    if form.validate_on_submit():
        # Username checking
        if User.query.filter_by(username=form.username.data).first():
            return jsonify({'error': 'Username already registered'}), 400
        
        # Email checking
        if User.query.filter_by(email=form.email.data).first():
            return jsonify({'error': 'Email already registered'}), 400
        
        # Initialize a new user with a hashed password
        user = User(username = form.username.data, email = form.email.data)
        user.set_password(form.password.data)
        
        # Added new user to the DB
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'message': 'User registered successfully!',
            'data': {'user_id': user.id}
        }), 201
    
    return jsonify({'error': form.errors}), 400