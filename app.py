from flask import Flask
from extensions import db
from routes.notes import notes_bp
from routes.auth import auth_bp

def create_app():
    app = Flask(__name__)

    # Configuration
    app.config['SECRET_KEY'] = 's6q3e4f5gfjeh901i2j3k4l5mrn0ohdp'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions
    db.init_app(app)
    
    # Registration of blueprints
    app.register_blueprint(notes_bp, url_prefix='/notes')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    @app.route('/')
    def index():
        return "It works!"
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)