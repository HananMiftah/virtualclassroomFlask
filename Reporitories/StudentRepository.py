from flask import Flask, request, Blueprint
from flask_marshmallow import Marshmallow
from flask_restplus import Api, Resource, fields
from flask_cors import CORS

from ..settings import *
from ..models import *
from ..ma import *


app = Flask(__name__)
CORS(app)

# app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS


db.init_app(app)
ma = Marshmallow(app)

api = Api(app, version='1.0', title='Virtual Classroom API',
          description='A simple Virtual Classroom API')
stuNS = api.namespace("Student")
student_schema = StudentSchema()
students_schema = StudentSchema(many=True)

blueprint = Blueprint('api', __name__)
api = Api(blueprint)

# Model required by flask_restplus for expect
student = api.model("Students", {
    'FirstName': fields.String(),
    'LastName': fields.String(),
    'Email': fields.String(),
})

#############################################
'''
STUDENT
'''
#############################################
@stuNS.route('/api/authenticate/students')
# @cross_origin()
class studentsResource(Resource):
    def get(self):
        '''
        Get Students Info
        '''
        students = Students.query.all()
        print(students)
        return students_schema.dump(students)

@stuNS.route('/api/authenticate/students/createstudent')
# @cross_origin()
class studentsResource(Resource):
    def post(self):
        '''
        Get Students Info
        '''
        students = Students.query.all()
        print(students)
        return students_schema.dump(students)

@stuNS.route('/api/authenticate/students/<int:stuID>')
class studentResource(Resource):
    def get(self,stuID):
        '''
        Get Student Info
        '''
        student = Students.query.filter_by(StudentID=stuID).first()
        print(student)
        return student_schema.dump(student)
    
    def patch(self,stuID):
        '''
        Edit Student Info
        '''
        student = Students.query.filter_by(StudentID=stuID).first()
        print(student)
        return student_schema.dump(student)

@stuNS.route('/api/authenticate/students/studentbyemail')
class studentsResources(Resource):
    def get(self):
        '''
        Get Students Info
        '''
        students = Students.query.all()
        print(students)
        return students_schema.dump(students)

@stuNS.route('/api/authenticate/students/studentbyemail/<int:studentEmail>')
class studentsResourcesOne(Resource):
    def get(self,studentEmail):
        '''
        Get Students Info
        '''
        students = Students.query.all()
        print(students)
        return students_schema.dump(students)

