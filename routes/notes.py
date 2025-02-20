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