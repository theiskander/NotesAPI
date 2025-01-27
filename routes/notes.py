from flask import Blueprint, request, jsonify
from models import Note
from datetime import datetime, timezone
from extensions import db

notes_bp = Blueprint('notes', __name__)

# Create a note
@notes_bp.route('/create', methods=['POST'])
def create():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid JSON payload'}), 400

    title = data.get('title')
    content = data.get('content')

    if not title:
        return jsonify({'error': 'Title is required'}), 400

    time = datetime.now(timezone.utc)
    
    new_note = Note(
        title=title,
        content=content,
        created_at=time,
        updated_at=time
    )
    db.session.add(new_note)
    db.session.commit()

    return jsonify({
        'message': 'Note created successfully',
        'note': {
            'id': new_note.id,
            'title': new_note.title,
            'content': new_note.content,
        }
    }), 201
    
# Get all notes
@notes_bp.route('/', methods=['GET'])
def get_notes():
    notes = Note.query.all()
    notes_list = []
    
    for note in notes:
        notes_list.append(
            {'id': note.id,
            'title': note.title,
            'content': note.content,
            'created_at': note.created_at,
            'updated_at': note.updated_at
            })
        
    return jsonify(notes_list)

# Get a note
@notes_bp.route('/<int:note_id>', methods=['GET'])
def get_note(note_id):
    note = Note.query.get(note_id)
    if not note:
        return jsonify({'error': 'Note not found'}), 404
    
    return jsonify({
        'message': 'Note created successfully',
        'note': {
            'id': note.id,
            'title': note.title,
            'content': note.content,
            'created_at': note.created_at,
            'updated_at': note.updated_at
        }
    })

# Update a not
@notes_bp.route('/<int:note_id>', methods=['PUT'])
def update_note(note_id):
    data = request.get_json()
    note = Note.query.get(note_id)
    if not note:
        return jsonify({'error': 'Note not found'}), 404
    
    note.title = data.get('title', note.title)
    note.content = data.get('content', note.content)
    note.updated_at = datetime.now(timezone.utc)
    
    if not data.get('title') and not data.get('content'):
        return jsonify({'error': 'No data provided for update'}), 400

    db.session.commit()
    return jsonify({'message': 'Note updated successfully',
                    'note': {
                        'id': note.id,
                        'title': note.title,
                        'content': note.content,
                        'updated_at': note.updated_at
        }
    })
    
# Delete a note
@notes_bp.route('/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    note = Note.query.get(note_id)
    if not note:
        return jsonify({'error': 'Note not found'}), 401
    
    db.session.delete(note)
    db.session.commit()
    return jsonify ({"message": 'deleted succesfully'})