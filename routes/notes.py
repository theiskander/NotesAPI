from flask import Blueprint, request, jsonify
from models import Note
from datetime import datetime, timezone
from extensions import db

notes_bp = Blueprint('notes', __name__)

@notes_bp.route('/create', methods=['POST'])
def create():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid JSON payload'}), 400

    title = data.get('title')
    content = data.get('content')

    if not title:
        return jsonify({'error': 'Title is required'}), 400

    new_note = Note(
        title=title,
        content=content,
        created_at=datetime.now(timezone.utc)
    )
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