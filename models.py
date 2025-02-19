from extensions import db
from datetime import datetime, timezone

class Note(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    content = db.Column(db.Text, nullable = True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable = False)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate = lambda: datetime.now(timezone.utc), nullable = False)
    
    def __repr__(self):
        return f"<Note {self.id}: {self.title}>"