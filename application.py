import re
from flask import Flask, request
from flask_marshmallow import Marshmallow
from flask_restplus import Api, Resource, fields
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash

from .settings import *
from .models import *
from .ma import *



app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS


db.init_app(app)
ma = Marshmallow(app)

api = Api(app, version='1.0', title='Virtual Classroom API',
          description='A simple Virtual Classroom API')
autNS = api.namespace("Authentication")
stuNS = api.namespace("Student")
insNS = api.namespace("Instructor")
resNS = api.namespace("Resource")
couNS = api.namespace("Course")
clsNS = api.namespace("Classroom")

student_schema = StudentSchema()
students_schema = StudentSchema(many=True)



# Model required by flask_restplus for expect
student = api.model("Students", {
    'FirstName': fields.String(),
    'LastName': fields.String(),
    'Email': fields.String(),
    'Password': fields.String(),
})

#############################################
'''
AUTHENTICATION
'''
#############################################

@autNS.route('/api/authenticate')
# @cross_origin()
class authentication(Resource):
    def get(self):
        return 

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
        return students_schema.dump(students)

@stuNS.route('/api/authenticate/students/createstudent')
class studentsResource(Resource):
    @api.expect(student)
    def post(self):
        '''
        Create a new Student
        '''
        new_student = Students()
        new_student.FirstName = request.json['FirstName']
        new_student.LastName = request.json['LastName']
        new_student.Email = request.json['Email']
        new_student.Password = generate_password_hash(request.json['Password'], method='sha256')

        db.session.add(new_student)
        db.session.commit()
        return student_schema.dump(new_student)

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
        return

@stuNS.route('/api/authenticate/students/studentbyemail')
class studentsResources(Resource):
    def get(self):
        return

@stuNS.route('/api/authenticate/students/studentbyemail/<int:studentEmail>')
class studentsResourcesOne(Resource):
    def get(self,studentEmail):
        return

#############################################
'''
INSTRUCTOR
'''
#############################################

@insNS.route('/api/authenticate/instructors')
class instructorsResource(Resource):
    def get(self):
        return

@insNS.route('/api/authenticate/instructors/createinstructor')
class instructorsResource(Resource):
    def post(self):
        return 


@insNS.route('/api/authenticate/instructors/<int:instructorID>')
class instructorResource(Resource):
    def get(self,instructorID):
        return
    
    def patch(self,instructorID):
        return

#############################################
'''
RESOURCE
'''
#############################################
@resNS.route('/api/courses/<int:courseID>/Resources')
class resourcesResource(Resource):
    def get(self,courseID):
        return

    def post(self,courseID):
        return

@resNS.route('/api/courses/<int:courseID>/resources/<int:resourceID>')
class resourceResource(Resource):
    def get(self,courseID,resourceID):
        return
    
    def delete(self,courseID,resourceID):
        return

@resNS.route('/api/courses/<int:courseID>/resources/<int:resourceID>/download')
class resourcesResourceOne(Resource):
    def get(self,courseID,resourceID):
        return

#############################################
'''
COURSE
'''
#############################################
@couNS.route('/api/courses')
class coursesResource(Resource):
    def post(self):
        return

@couNS.route('/api/courses/<int:courseID>')
class courseResource(Resource):
    def get(self,courseID):
        return
    
    def post(self,courseID):
        return
    
    def patch(self,courseID):
        return

@couNS.route('/api/courses/<int:courseID>/student/<int:ids>')
class courseResourceOne(Resource):
    def get(self,courseID,ids):
        return
    
@couNS.route('/api/courses/<int:courseID>/students')
class courseResourceTwo(Resource):
    def get(self,courseID):
        return

@couNS.route('/api/courses/studentcourses')
class courseResourceThree(Resource):
    def get(self):
        return

@couNS.route('/api/courses/studentcourses/<int:courseID>')
class courseResourceFour(Resource):
    def get(self,courseID):
        return

@couNS.route('/api/courses/instructorcourses')
class courseResourceFive(Resource):
    def get(self):
        return
    
#############################################
'''
CLASSROOM
'''
#############################################

@clsNS.route('/api/courses/<int:courseID>/classrooms/<int:classroomID>')
class classroomResource(Resource):
    def get(self,courseID,classroomID):
        return
    
    def patch(self,courseID,classroomID):
        return

@clsNS.route('/api/courses/<int:courseID>/classrooms')
class classroomResourceOne(Resource):
    def get(self,courseID):
        return
    
    def post(self,courseID):
        return
    
@clsNS.route('/api/courses/<int:courseID>/classrooms/<int:classroomID>/join')
class classroomResourceTwo(Resource):
    def get(self,courseID,classroomID):
        return
