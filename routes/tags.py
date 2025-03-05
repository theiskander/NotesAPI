from flask import Blueprint, request, jsonify, session

from utils.auth_helper import check_access, check_user
from models import Tag
from extensions import db

tags_bp = Blueprint('tags', __name__)

# Create a tag
@tags_bp.route('/create', methods = ['GET'])
def create_tag():
    # Authorization check
    access = check_access(True)
    if access:
        return access
    
    # Date request
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid JSON payload'}), 400
    
    # Fill in in the fields of a new tag
    name = data.get('name')
    if not name:
        return jsonify({'error': 'Name is required'}), 400
    user_id = session['user_id']
    
    # Check a name
    if Tag.query.filter_by(name = name, user_id = user_id).first():
        return jsonify({'error': 'Tag with this name already created by you'}), 400
    
    # Creating new tag
    new_tag = Tag(
        name = name,
        user_id = user_id
    )
    
    # Add new tag to the DB
    db.session.add(new_tag)
    db.session.commit()
    
    return jsonify({
        'message': 'The tag created successfully',
        'tag': {
            'name': new_tag.name,
            'user_id': new_tag.user_id
        }
    }), 201