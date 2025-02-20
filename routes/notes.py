from flask import Blueprint, request, jsonify
from models import Note
from datetime import datetime, timezone
from extensions import db

notes_bp = Blueprint('notes', __name__)

# Create a note
@notes_bp.route('/create', methods=['POST'])
def create():
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
    
    # Creating a note
    new_note = Note(
        title=title,
        content=content,
        created_at=time,
        updated_at=time
    )
    
    # Added a note to the DB
    db.session.add(new_note)
    db.session.commit()

    return jsonify({
        'message': 'Note created successfully',
        'note': {
            'id': new_note.id,
            'title': new_note.title,
            'content': new_note.content
        }
    }), 201

# Get all notes
@notes_bp.route('/', methods=['GET'])
def get_notes():
    # Search notes and retrieve data from them
    notes = Note.query.all()
    notes_list = []
    
    # Creating a list of all notes
    for note in notes:
        notes_list.append({
            'id': note.id,
            'title': note.title,
            'content': note.content,
            'created_at': note.created_at,
            'updated_at': note.updated_at
        })
        
    return jsonify(notes_list), 200

@notes_bp.route('/<int:note_id>', methods=['GET'])
def get_note(note_id):
    # Search for a note
    note = Note.query.get(note_id)
    if not note:
        return jsonify({'error': 'Note not found'}), 404
    
    return jsonify({
        'message': 'Note found successfully',
        'note': {
            'id': note.id,
            'title': note.title,
            'content': note.content,
            'created_at': note.created_at,
            'updated_at': note.updated_at
        }
    }), 200
    
@notes_bp.route('/<int:note_id>', methods=['PUT'])
def update_note(note_id):
    # Data request
    data = request.get_json()
    
    # Search for a note
    note = Note.query.get(note_id)
    if not note:
        return jsonify({'error': 'Note not found'}), 404
    
    # Updating fields
    note.title = data.get('title', note.title)
    note.content = data.get('content', note.content)
    if not data.get('title') and not data.get('content'):
        return jsonify({'error': 'No data provided for update'}), 400
    note.updated_at = datetime.now(timezone.utc)
    
    # Updating a note in the DB
    db.session.commit()
    
    return jsonify({'message': 'Note updated successfully',
                    'note': {
                        'id': note.id,
                        'title': note.title,
                        'content': note.content,
                        'created_at': note.created_at,
                        'updated_at': note.updated_at
                    }
            })

