from flask import Blueprint, jsonify, request
from forms import RegistrationForm
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
            return jsonify({'success': False, 'message': 'Email already registered'}), 400
        
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