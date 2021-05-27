import csv

from flask import Flask,render_template,request
from models import *
from settings import *

app = Flask(__name__)

app.config['SERVER_NAME'] = FLASK_SERVER_NAME
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS

db.init_app(app)

def main():
    if __name__ == '__main__':
        with app.app_context():
            main()