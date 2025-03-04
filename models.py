from extensions import db
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash

class Note(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    content = db.Column(db.Text, nullable = True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable = False)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate = lambda: datetime.now(timezone.utc), nullable = False)
    
    # Foreign Keys
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable = False)
    
    def __repr__(self):
        return f'<Note {self.id}: {self.title}>'
    
class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(32), unique = True, nullable = False)
    email = db.Column(db.String(64), unique = True, nullable = False)
    password_hash = db.Column(db.String(128), nullable = False)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
class Category(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(32), unique = True, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)

    # Uniqueness within an user
    __table_args__ = (db.UniqueConstraint('name', 'user_id', name = 'uq_category_name_for_user'),)
    
    # Relationship 1:m
    notes = db.relationship('Note', backref = 'category', cascade = 'all, delete-orphan')
    
# Retrieve or creating Uncategorized category  
def ensure_uncategorized_exists():
    #Search for the category
    category = Category.query.filter_by(name = 'Uncategorized').first()
    
    # Create the category
    if not category:
        uncategorized = Category(id = 0, name = 'Uncategorized', user_id = 0)
        db.session.add(uncategorized)
        db.session.commit()
