from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = 's6q3e4f5gfjeh901i2j3k4l5mrn0ohdc'
    
    @app.route('/')
    def index():
        return "It works!"
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)