from flask import Flask, request, flash
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from VirtualClassroom.config import *
from flask_socketio import SocketIO
from VirtualClassroom.Socket.VirtualClass import register_websocket

db = SQLAlchemy()
cors = CORS(resources={r"/*":{"origins":"*"}})
ma = Marshmallow()

def create_app():
    from VirtualClassroom.Resources import blueprint, init_api
    init_api()
    app = Flask(__name__)
    socket_io = SocketIO(app, cors_allowed_origins="*")
    register_websocket(socket_io)
    app.register_blueprint(blueprint, url_prefix='/api')


    db_uri = SQLALCHEMY_DATABASE_URI
    if db_uri.startswith("postgres://"):
        db_uri = db_uri.replace("postgres://", "postgresql://", 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
    app.debug = True

    cors.init_app(app)
    db.init_app(app)
    ma.init_app(app)

    return app, socket_io
