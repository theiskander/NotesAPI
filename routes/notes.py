from flask import Blueprint

notes_bp = Blueprint('notes', __name__)

@notes_bp.route('/create', methods=['GET'])
def create():
	return "Create route here!"