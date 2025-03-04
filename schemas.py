from extensions import ma
from models import Note, Category

class NoteSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Note
    
    # Autofields for connection
    id = ma.auto_field()
    title = ma.auto_field()
    content = ma.auto_field()
    created_at = ma.auto_field()
    updated_at = ma.auto_field()
    category_id = ma.auto_field()

class CategorySchema(ma.SQLAlchemySchema):
    class Meta:
        model = Category
    
    # Autofields for connection
    id = ma.auto_field()
    name = ma.auto_field()
    
# Instances of the Note schema
note_schema = NoteSchema()
notes_schema = NoteSchema(many = True)

# Instances of the Category schema
category_schema = CategorySchema()
categories_schema = CategorySchema(many = True)