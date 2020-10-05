import os


class Config:
    DEBUG = False
    # Что это?
    CSRF_ENABLED = True
    # Ключ для подписи данных.
    SECRET_KEY = 'super-secret'
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
