import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    DB_USER = os.getenv('DB_USER', 'admin')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'password')
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_NAME = os.getenv('DB_NAME', 'shopdb')
    
    ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
    
    if ENVIRONMENT == 'production':
        SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    else:
        SQLALCHEMY_DATABASE_URI = 'sqlite:///shop.db'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    APP_VERSION = os.getenv('APP_VERSION', '1.0.0')
    APP_NAME = 'TechShop'