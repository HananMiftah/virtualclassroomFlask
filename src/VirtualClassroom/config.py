import os
class Config:

    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    # SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:root@localhost/virtualclassdb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_BLACKLIST_ENABLED = ['access']
    UPLOAD_FOLDER = './../../static'
