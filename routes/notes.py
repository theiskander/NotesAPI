from flask import Blueprint, request, jsonify, session
from datetime import datetime, timezone

from models import Note
from schemas import note_schema, notes_schema

from extensions import db
from utils.auth_helper import check_access, check_user

notes_bp = Blueprint('notes', __name__)

# Create a note
@notes_bp.route('/create', methods=['POST'])
def create():
    # Authorization check
    access = check_access(True)
    if access: return access
    
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
    
    # Creating a note
    new_note = Note(
        title=title,
        content=content,
        created_at=time,
        updated_at=time,
        user_id = user_id
    )
    
    # Added a note to the DB
    db.session.add(new_note)
    db.session.commit()

    return jsonify({
        'message': 'Note created successfully',
        'note': note_schema.dump(new_note)
    }), 201

# Get all notes
@notes_bp.route('/', methods=['GET'])
def get_notes():
    # Authorization check
    access = check_access(True)
    if access: return access
    
    # Search notes and retrieve data from them
    notes = Note.query.filter_by(user_id=session['user_id']).all()
    if not notes:
        return jsonify({'error': 'Notes not found'}), 404
      
    return jsonify({
        'message': 'Notes list',
        'note': notes_schema.dump(notes)
    }), 200

# Get a note by id
@notes_bp.route('/<int:note_id>', methods=['GET'])
def get_note(note_id):
    # Authorization check
    access = check_access(True)
    if access: return access
    
    # Search for a note
    note = Note.query.get(note_id)
    if not note:
        return jsonify({'error': 'Note not found'}), 404
    
    # Check note owner
    owner = check_user(note)
    if owner: return owner
    
    return jsonify({
        'message': 'Note have found successfully',
        'note': note_schema.dump(note)
    }), 200

# Update a note by id
@notes_bp.route('/<int:note_id>', methods=['PUT'])
def update_note(note_id):
    # Authorization check
    access = check_access(True)
    if access: return access
    
    # Data request
    data = request.get_json()
    
    # Search for a note
    note = Note.query.get(note_id)
    if not note:
        return jsonify({'error': 'Note not found'}), 404
    
    # Check note owner
    owner = check_user(note)
    if owner: return owner
    
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
@notes_bp.route('/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    # Authorization check
    access = check_access(True)
    if access: return access
    
    # Search for a note
    note = Note.query.get(note_id)
    if not note:
        return jsonify({'error': 'Note not found'}), 401
    
    # Check note owner
    owner = check_user(note)
    if owner: return owner
    
    # Creating a response
    deleted_note = note_schema.dump(note)
    
    # Deleting a note from the DB
    db.session.delete(note)
    db.session.commit()
    
    return jsonify ({
        "message": 'Note DELETED succesfully',
        'deleted': deleted_note
    }), 202