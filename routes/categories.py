from flask import Blueprint, jsonify, request, session

from models import Category
from extensions import db
from utils.auth_helper import check_access, check_user
from schemas import category_schema, categories_schema

categories_bp = Blueprint('categories', __name__)

# Create a category
@categories_bp.route('/create', methods = ['POST'])
def create_category():
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
    if Category.query.filter_by(name = name, user_id = user_id).first():
        return jsonify({'error': 'Category with this name already created by you'}), 400
    
    # Creating a new category
    new_category = Category(
        name = name,
        user_id = user_id
    )
    
    # Add new category to the DB
    db.session.add(new_category)
    db.session.commit()
    
    return jsonify({
        'message': 'The category created successfully',
        'category': category_schema.dump(new_category)
    }), 201

# All categories by user_id
@categories_bp.route('/', methods = ['GET'])
def get_categories():
    # Authorization check
    access = check_access(True)
    if access:
        return access
    
    # Search categories and retrieve data from them
    categories = Category.query.filter_by(user_id = session['user_id']).all()
    if not categories:
        return jsonify({
        'message': 'You have only Uncategorized category (by default)',
        }), 200
    
    return jsonify({
        'message': 'Categories list',
        'categories': categories_schema.dump(categories)
    }), 200

# Update a category
@categories_bp.route('/<int:category_id>', methods = ['PUT'])
def update_category(category_id):
    # Authorization check
    access = check_access(True)
    if access:
        return access
    
    # Data request
    data = request.get_json()
    
    # Check existing of name
    name = data.get('name')
    if not name:
        return jsonify({'error': 'No data for update'}), 400
    
    # Search for a category
    category = Category.query.get(category_id)
    if not category:
        return jsonify({'error': 'Category not found'}), 404
    
    # Check category owner
    owner = check_user(category)
    if owner:
        return owner
    
    # Check for the uniqueness of the category name
    existing_category = Category.query.filter_by(name = name).first()
    if existing_category and existing_category.id != category_id:
        return jsonify({'error': 'Category with this name already created by you'}), 400
    
    # Updating a name
    category.name = name
    
    # Updating a DB
    db.session.commit()
    
    return jsonify({
        'message': 'The category updated successfully',
        'category': category_schema.dump(category)
    }), 200

# Delete a category
@categories_bp.route('/<int:category_id>', methods = ['DELETE'])
def delete_category(category_id):
    # Authorization check
    access = check_access(True)
    if access:
        return access
    
    # Search for a category
    category = Category.query.get(category_id)
    if not category:
        return jsonify({'error': 'Category not found'}), 404
    
    # Check category owner
    owner = check_user(category)
    if owner:
        return owner

    # Creating a response
    deleted_category = category

    # Delete a category from DB
    db.session.delete(category)
    db.session.commit()
    
    return jsonify({
        'message': 'The category was DELETED',
        'deleted': category_schema.dump(deleted_category)
    }), 202 