from flask import Blueprint, jsonify, request, session

from models import Category
from extensions import db
from utils.auth_helper import check_access

categories_bp = Blueprint("categories", __name__)

@categories_bp.route('/create', methods = ['POST'])
def categories():
    # Authorization check
    access = check_access(True)
    if access:
        return access
    
    # Data request
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid JSON payload'}), 400
    
     # Fill in in the fields of a new category
    user_id = session['user_id']
    name = data.get('name')
    if not name:
        return jsonify({'error': 'Name is required'}), 400
    
    # Check avalability of a name
    if Category.query.filter_by(name=name).first():
        return jsonify({'error': 'Name already registered'}), 400
    
    # Creating a new category
    new_category = Category(
        name = name,
        user_id = user_id
    )
    
    # Add new note to the DB
    db.session.add(new_category)
    db.session.commit()
    
    return jsonify({
        'message': 'The category created successfully',
        'category': {
            'id': new_category.id,
            'name': new_category.name
            }
    }), 201