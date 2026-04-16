"""
Configuration Module for Event Management System
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = False
    TESTING = False
    
    # PostgreSQL/Supabase Configuration
    DATABASE_URL = os.getenv('DATABASE_URL', '')
    # Fallback to individual connection parameters
    POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
    POSTGRES_USER = os.getenv('POSTGRES_USER', 'postgres')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', '')
    POSTGRES_DB = os.getenv('POSTGRES_DB', 'postgres')
    POSTGRES_PORT = int(os.getenv('POSTGRES_PORT', 5432))
    
    # Session Configuration
    SESSION_TIMEOUT = int(os.getenv('SESSION_TIMEOUT', 3600))
    PERMANENT_SESSION_LIFETIME = SESSION_TIMEOUT
    
    # Razorpay Configuration
    RAZORPAY_KEY_ID = os.getenv('RAZORPAY_KEY_ID', '')
    RAZORPAY_KEY_SECRET = os.getenv('RAZORPAY_KEY_SECRET', '')
    
    # File Upload Configuration
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'app', 'static', 'uploads')
    CERTIFICATE_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'certificates')
    
    # Face Recognition Configuration
    FACE_ENCODING_MODEL = 'small'  # 'small' or 'large'
    FACE_DISTANCE_THRESHOLD = 0.6


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = False
    TESTING = False


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False


class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    MYSQL_DB = 'event_management_test'


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config(env=None):
    """Get configuration based on environment"""
    if env is None:
        env = os.getenv('FLASK_ENV', 'development')
    return config.get(env, config['default'])
