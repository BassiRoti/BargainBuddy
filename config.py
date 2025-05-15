import os

class Config:
    # Database
    SQLALCHEMY_DATABASE_URI = 'mysql://bargainbuddy:BargainBuddy@localhost:3307/bargainbuddy'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Security
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-please-change-in-production'
    
    # File Upload
    UPLOAD_FOLDER = os.path.join('app', 'static', 'uploads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # Session
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hour
    
    # Debug
    DEBUG = True
