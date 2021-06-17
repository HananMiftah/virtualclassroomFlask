import re
from flask import Blueprint
from flask_restplus import Api
from VirtualClassroom.config import *
from VirtualClassroom.schemas import *
from VirtualClassroom.models import *


def init_api():
    from VirtualClassroom.Resources.classroom import ClassroomNamspace
    from VirtualClassroom.Resources.Authentication import AuthenticationNamespace
    from VirtualClassroom.Resources.Student import StudentNamespace
    from VirtualClassroom.Resources.Instructor import InstructorsNamespace
    from VirtualClassroom.Resources.Course import CourseNamespace
    from VirtualClassroom.Resources.Resource import ResourceNamespace

    

blueprint = Blueprint('api_v1', __name__)

api = Api(blueprint, version='1.0', title='Virtual Classroom API',
          description='A simple Virtual Classroom API')
