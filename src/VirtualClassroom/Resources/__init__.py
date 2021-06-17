import re
from flask import Blueprint
from flask_restplus import Api
from src.VirtualClassroom.config import *
from src.VirtualClassroom.schemas import *
from src.VirtualClassroom.models import *


def init_api():
    from src.VirtualClassroom.Resources.classroom import ClassroomNamspace
    from src.VirtualClassroom.Resources.Authentication import AuthenticationNamespace
    from src.VirtualClassroom.Resources.Student import StudentNamespace
    from src.VirtualClassroom.Resources.Instructor import InstructorsNamespace
    from src.VirtualClassroom.Resources.Course import CourseNamespace
    from src.VirtualClassroom.Resources.Resource import ResourceNamespace

    

blueprint = Blueprint('api_v1', __name__)

api = Api(blueprint, version='1.0', title='Virtual Classroom API',
          description='A simple Virtual Classroom API')
