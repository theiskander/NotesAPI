from flask import Blueprint, request, jsonify, session

from utils.auth_helper import check_access, check_user
from models import Tag
from extensions import db

tags_bp = Blueprint('tags', __name__)

# Create a tag
@tags_bp.route('/create', methods = ['POST'])
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
    
# Retrieve all tags by user id
@tags_bp.route('/', methods = ['GET'])
def get_tags():
    # Authorization check
    access = check_access(True)
    if access:
        return access
    
    # Search for tags
    tags = Tag.query.filter_by(user_id = session['user_id']).all()
    if not tags:
        return jsonify({'error': 'Tags not found',}), 404
    
    # Creating a list of all tags
    tags_list = []
    for tag in tags:
        tags_list.append({
            'name': tag.name,
            'id': tag.id
        })
        
    return jsonify({
        'message': 'Tags list',
        'tags': tags_list
    }), 200

# Update a tag
@tags_bp.route('/<int:tag_id>', methods = ['PUT'])
def update_tag(tag_id):
    # Authorization check
    access = check_access(True)
    if access:
        return access
    
    # Data request
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid JSON payload'}), 400
    
    # Check existing of name
    name = data.get('name')
    if not name:
        return jsonify({'error': 'No data for update'}), 400
    
    # Search for a tag
    tag = Tag.query.get(tag_id)
    if not tag:
        jsonify({'error':'The tag not found'}), 404
        
    # Check tag owner
    owner = check_user(tag)
    if owner:
        return owner
    
    # Check for the uniqueness of the tag name
    existing_tag = Tag.query.filter_by(name = name).first()
    if existing_tag and existing_tag.id != tag_id:
        return jsonify({'error': 'The tag with this name already created by you'}), 400
    
    # Updating a name
    tag.name = name
    
    # Updating a DB
    db.session.commit()
    
    return jsonify({
        'message': 'The tag updated successfully',
        'tag': {
            'name': tag.name,
            'id': tag.id
        }
    }), 200