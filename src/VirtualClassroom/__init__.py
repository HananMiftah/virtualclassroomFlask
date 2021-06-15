from flask import Flask, request, flash
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from VirtualClassroom.config import *

db = SQLAlchemy()
cors = CORS()
ma = Marshmallow()

def create_app():
    from VirtualClassroom.Resources import blueprint, init_api
    init_api()
    app = Flask(__name__)
    app.register_blueprint(blueprint, url_prefix='/api')

    jwt=JWTManager(app)
    db_uri = SQLALCHEMY_DATABASE_URI
    if db_uri.startswith("postgres://"):
        db_uri = db_uri.replace("postgres://", "postgresql://", 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
    app.debug = True

    cors.init_app(app)
    db.init_app(app)
    ma.init_app(app)

    return app

