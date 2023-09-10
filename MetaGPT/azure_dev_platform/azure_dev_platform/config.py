## config.py
import os
from typing import Tuple

class Config:
    """Configuration class for the Flask application and the database connection."""

    SECRET_KEY: str = os.environ.get('SECRET_KEY') or 'hard_to_guess_string'
    SQLALCHEMY_DATABASE_URI: str = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    AZURE_SUBSCRIPTION_ID: str = os.environ.get('AZURE_SUBSCRIPTION_ID')
    AZURE_TENANT_ID: str = os.environ.get('AZURE_TENANT_ID')
    AZURE_CLIENT_ID: str = os.environ.get('AZURE_CLIENT_ID')
    AZURE_CLIENT_SECRET: str = os.environ.get('AZURE_CLIENT_SECRET')

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    """Development configuration class."""

    DEBUG: bool = True

class TestingConfig(Config):
    """Testing configuration class."""

    TESTING: bool = True

class ProductionConfig(Config):
    """Production configuration class."""

    DEBUG: bool = False

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
