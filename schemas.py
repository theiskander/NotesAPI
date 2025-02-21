from extensions import ma
from models import Note

class NoteSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Note
    
    # Autofields for connection
    id = ma.auto_field()
    title = ma.auto_field()
    content = ma.auto_field()
    created_at = ma.auto_field()
    updated_at = ma.auto_field()

# Instances of the schema
note_schema = NoteSchema()
notes_schema = NoteSchema(many=True)