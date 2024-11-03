import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_fallback_key')
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{os.getenv('DATABASE_USER')}:{os.getenv('DATABASE_PASSWORD')}@{os.getenv('DATABASE_HOST')}/{os.getenv('DATABASE_NAME')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Email configurations
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('EMAIL_USER')
    MAIL_PASSWORD = os.getenv('EMAIL_PASS')
