from flask import Blueprint, request, jsonify, session
from datetime import datetime, timezone
from sqlalchemy import delete

from models import Note, Tag
from schemas import note_schema, notes_schema, tag_schema

from extensions import db
from utils.auth_helper import check_access, check_user

notes_bp = Blueprint('notes', __name__)

# Create a note
@notes_bp.route('/create', methods = ['POST'])
def create():
    # Authorization check
    access = check_access(True)
    if access:
        return access
    
    # Data request
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid JSON payload'}), 400

    # Fill in the fields of a new note
    title = data.get('title')
    if not title:
        return jsonify({'error': 'Title is required'}), 400
    content = data.get('content')
    time = datetime.now(timezone.utc)
    user_id = session['user_id']
    category_id = data.get('category_id')
    if not category_id:
        category_id = 0
    
    # Creating a note
    new_note = Note(
        title = title,
        content = content,
        created_at = time,
        updated_at = time,
        user_id = user_id,
        category_id = category_id
    )
    
    # Added a note to the DB
    db.session.add(new_note)
    db.session.commit()

    return jsonify({
        'message': 'Note created successfully',
        'note': note_schema.dump(new_note)
    }), 201

# Get all notes
@notes_bp.route('/', methods = ['GET'])
def get_notes():
    # Authorization check
    access = check_access(True)
    if access:
        return access
    
    # Search notes and retrieve data from them
    notes = Note.query.filter_by(user_id=session['user_id']).all()
    if not notes:
        return jsonify({'error': 'Notes not found'}), 404
      
    return jsonify({
        'message': 'Notes list',
        'note': notes_schema.dump(notes)
    }), 200

# Get a note by id
@notes_bp.route('/<int:note_id>', methods = ['GET'])
def get_note(note_id):
    # Authorization check
    access = check_access(True)
    if access:
        return access
    
    # Search for a note
    note = Note.query.get(note_id)
    if not note:
        return jsonify({'error': 'Note not found'}), 404
    
    # Check note owner
    owner = check_user(note)
    if owner:
        return owner
    
    return jsonify({
        'message': 'Note have found successfully',
        'note': note_schema.dump(note)
    }), 200

# Update a note by id
@notes_bp.route('/<int:note_id>', methods = ['PUT'])
def update_note(note_id):
    # Authorization check
    access = check_access(True)
    if access:
        return access
    
    # Data request
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid JSON payload'}), 400
    
    # Search for a note
    note = Note.query.get(note_id)
    if not note:
        return jsonify({'error': 'Note not found'}), 404
    
    # Check note owner
    owner = check_user(note)
    if owner:
        return owner
    
    # Updating fields
    note.title = data.get('title', note.title)
    note.content = data.get('content', note.content)
    if not data.get('title') and not data.get('content'):
        return jsonify({'error': 'No data provided for update'}), 400
    note.updated_at = datetime.now(timezone.utc)
    
    # Updating a note in the DB
    db.session.commit()

    return jsonify({
        'message': 'Note updated successfully',
        'note': note_schema.dump(note)
    }), 200

# Delete a note by id
@notes_bp.route('/<int:note_id>', methods = ['DELETE'])
def delete_note(note_id):
    # Authorization check
    access = check_access(True)
    if access:
        return access
    
    # Search for a note
    note = Note.query.get(note_id)
    if not note:
        return jsonify({'error': 'Note not found'}), 401
    
    # Check note owner
    owner = check_user(note)
    if owner:
        return owner
    
    # Creating a response
    deleted_note = note_schema.dump(note)
    
    # Deleting a note from the DB
    db.session.delete(note)
    db.session.commit()
    
    return jsonify ({
        'message': 'Note DELETED succesfully',
        'deleted': deleted_note
    }), 202
    
# Add a tag to a note
@notes_bp.route('/<int:note_id>/tags', methods = ['POST'])
def add_tag(note_id):
    # Authorization check
    access = check_access(True)
    if access:
        return access
    
    # Retrieve a data
    data = request.get_json()
    tag_id = data.get('tag_id')
    if not tag_id:
        return jsonify({'error': 'Invalid JSON payload'}), 400
    
    # Search for a note
    note = Note.query.get(note_id)
    if not note:
        return jsonify({'error': 'The note was not found'}), 404
    
    # Check a note owner
    owner = check_user(note)
    if owner:
        return owner
    
    # Search for a tag
    tag = Tag.query.get(tag_id)
    if not tag:
        return jsonify({'error': 'The tag was not found'})
    
    # Check a tag owner
    owner = check_user(tag)
    if owner:
        return owner
    
    # Creating a record
    new_record = Tag.note_tag.insert().values(
        note_id = note_id,
        tag_id = tag_id
    )
    
    # Add new record to the DB
    db.session.execute(new_record)
    db.session.commit()
    
    return jsonify({
        'notetag': {
            'note_id': note_id,
            'tag_id': tag_id
        }
    }), 201
    
# Delete a tag from a note
@notes_bp.route('/<int:note_id>/tags/<int:tag_id>', methods = ['DELETE'])
def remove_tag(note_id, tag_id):
    # Authorization check
    access = check_access(True)
    if access:
        return access
    
    # Search for a note
    note = Note.query.get(note_id)
    if not note:
        return jsonify({'error': 'The note was not found'}), 404
    
    # Search for a tag
    tag = Tag.query.get(tag_id)
    if not tag:
        return jsonify({'error': 'The tag was not found'}), 404

    # Check a tag owner
    owner = check_user(tag)
    if owner:
        return owner
    
    # Deleted tag from a note (JSON response before deletion)
    deleted_tag = tag_schema.dump(tag)

    # Deleting record from note_tag
    temp = delete(Tag.note_tag).where(
        (Tag.note_tag.c.note_id == note_id) & 
        (Tag.note_tag.c.tag_id == tag_id)
    )
    db.session.execute(temp)
    db.session.commit()
    
    return jsonify({
        'message': "The tag was DELETED successfully",
        'deleted_tag': deleted_tag
    }), 202