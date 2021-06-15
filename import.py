import csv

from flask import Flask,render_template,request
from models import *
from settings import *

app = Flask(__name__)

app.config['SERVER_NAME'] = FLASK_SERVER_NAME
db_uri = SQLALCHEMY_DATABASE_URI
if db_uri.startswith("postgres://"):
    db_uri = db_uri.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS

db.init_app(app)

def main():
    if __name__ == '__main__':
        with app.app_context():
            main()