import re
from flask import Flask, request, flash, Blueprint
from flask_marshmallow import Marshmallow
from flask_restplus import Api, Resource, fields
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from VirtualClassroom.config import *
from VirtualClassroom.schemas import *
from VirtualClassroom.models import *
import json


def init_api():
    from VirtualClassroom.Resources.classroom import ClassroomNamspace

blueprint = Blueprint('api_v1', __name__)

api = Api(blueprint, version='1.0', title='Virtual Classroom API',
          description='A simple Virtual Classroom API')
