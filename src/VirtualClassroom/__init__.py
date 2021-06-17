from flask import Flask, request, flash
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from VirtualClassroom.config import *
from flask_socketio import SocketIO
from VirtualClassroom.Socket.VirtualClass import register_websocket


db = SQLAlchemy()
cors = CORS(resources={r"/*":{"origins":"*"}})
ma = Marshmallow()

def create_app(config_class=Config):
    from VirtualClassroom.Resources import blueprint, init_api
    init_api()
    app = Flask(__name__)
    socket_io = SocketIO(app, cors_allowed_origins="*")
    register_websocket(socket_io)
    app.register_blueprint(blueprint, url_prefix='/api')
    app.config.from_object(Config)
    jwt=JWTManager(app)
    cors.init_app(app,allow_headers='*')
    db.init_app(app)
    ma.init_app(app)

    return app, socket_io
