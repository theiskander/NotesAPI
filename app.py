from flask import Flask

from extensions import db, ma
from routes.notes import notes_bp
from routes.auth import auth_bp
from routes.categories import categories_bp
from models import ensure_uncategorized_exists

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = 's6q3e4f5gfjeh901i2j3k4l5mrn0ohdc'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize of extensions
    db.init_app(app)
    ma.init_app(app)
    
    # Registration of blueprints
    app.register_blueprint(notes_bp, url_prefix = '/notes')
    app.register_blueprint(auth_bp, url_prefix = '/auth')
    app.register_blueprint(categories_bp, url_prefix = '/categories')
   
    # The DB initialization and creating the necessary records
    with app.app_context():
        db.create_all()
        ensure_uncategorized_exists()
   
    @app.route('/')
    def index():
        return 'It works!'

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)