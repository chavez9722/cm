from flask import Flask
from .models import db
from .routes import main

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    db.init_app(app)
    with app.app_context():
        db.create_all()  # Crea la tabla si no existe
    
    app.register_blueprint(main)

    return app
