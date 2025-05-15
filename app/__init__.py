from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, template_folder="templates")

    # Load configuration
    app.config.from_object("config.Config")

    # Initialize database
    db.init_app(app)

    from app.models import User 

    login_manager = LoginManager(app)
    login_manager.login_view = 'login'  # Redirect unauthorized users to login page

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Import routes
    from app.routes import init_routes
    init_routes(app)

    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()

    # File upload configuration
    UPLOAD_FOLDER = os.path.join('app', 'static','uploads')
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    # Ensure the upload folder exists
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    return app