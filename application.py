import re
from flask import Flask, request, flash
from flask_marshmallow import Marshmallow
from flask_restplus import Api, Resource, fields,reqparse
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash

from settings import *
from models import *
from ma import *
import json
from flask_jwt_extended import JWTManager
from flask_jwt_extended import ( create_access_token, get_jwt,
                            jwt_required, get_jwt_identity)
from datetime import timedelta


app = Flask(__name__)
CORS(app)
jwt=JWTManager(app)
db_uri = SQLALCHEMY_DATABASE_URI
if db_uri.startswith("postgres://"):
    db_uri = db_uri.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['JWT_SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['JWT_BLACKLIST_ENABLED'] = ['access']
app.debug = True

db.init_app(app)
ma = Marshmallow(app)

api = Api(app, version='1.0', title='Virtual Classroom API',
          description='A simple Virtual Classroom API')

AuthenticationNamespace = api.namespace("Authentication", path="/api/authenticate")
StudentNamespace = api.namespace("Student", path="/api/authenticate/students")
InstructorsNamespace = api.namespace("Instructor", path="/api/authenticate/instructors")
ClassroomNamspace = api.namespace("Classroom", path="/api/courses")
ResourceNamespace = api.namespace("Resource", path="/api/courses")
CourseNamespace = api.namespace("Course", path="/api/courses")


student_schema = StudentSchema()
students_schema = StudentSchema(many=True)

instructor_schema = InstructorSchema()
instructors_schema = InstructorSchema(many=True)

course_schema = CourseSchema()
course_schema = CourseSchema(many=True)


# Model required by flask_restplus for expect
student = api.model("Students", {
    'FirstName': fields.String(),
    'LastName': fields.String(),
    'Email': fields.String(),
    'Password': fields.String(),
})

instructor = api.model("Instructors", {
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

AuthenticationNamespace = api.namespace("Authentication", path="/api/authenticate")

user_auth_arguments = reqparse.RequestParser()
user_auth_arguments.add_argument('username', type=str, help="Username", required=True)
user_auth_arguments.add_argument('password', type=str, help="Password", required=True)

userCred = api.model("UserCred", {
    'UserName': fields.String(),
    'Password': fields.String() 
})

@AuthenticationNamespace.route('')
# @cross_origin()

class authentication(Resource):
    @api.expect(userCred)
    def post(self):
        print("\n\n\nhere\n\n\n")
        # args = user_auth_arguments.parse_args()
        username = request.json['UserName']
        password = request.json['Password']
        print("\n\n\nhere\n\n\n")

        user=Students.query.filter_by(Email=username).first()
        role="Student"
        print("\n\n\1\n\n\n")

        if user and  check_password_hash(user.Password , password):
            print("\n\n\2\n\n\n")
            
            expires = timedelta(days=30)
            additional_claims = {"role": role}
            token = create_access_token(
                identity=user.StudentID, 
                expires_delta=expires,
                additional_claims=additional_claims)
            return {'token': token}
        user=Instructors.query.filter_by(Email=username).first()
        role="Instrucotr"
        print("\n\n\3\n\n\n")

        if user and  check_password_hash(user.Password , password):
            print("\n\n\4\n\n\n")

            expires = timedelta(days=30)
            additional_claims = {"role": role}
            token = create_access_token(
                identity=user.InstructorID, 
                expires_delta=expires,
                additional_claims=additional_claims)
            return {'token': token}
        return "Incorrect Username or password" ,401


#############################################
'''
STUDENT
'''
#############################################

@StudentNamespace.route('/createstudent')
class Student(Resource):
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

        student = Students.query.filter_by(Email=new_student.Email).first()
        if student:
            return "Email already taken", 400

        db.session.add(new_student)
        db.session.commit()
        return student_schema.dump(new_student), 201

@StudentNamespace.route('/<int:stuID>')
class studentResource(Resource):
    def get(self,studentId):
        '''
        Get Student Info
        '''
        student = Students.query.filter_by(StudentID=studentId).first()

        if student:
            return student_schema.dump(student)
        return "Student not found",404
    @api.expect(student)
    def patch(self,studentId):
        '''
        Edit Student Info
        '''
        student = Students.query.filter_by(StudentID=studentId).first()

        #updating required fields
        for key in request.json.keys():
            if key == 'FirstName':
                student.FirstName = request.json[key]
            elif key == 'LastName':
                student.LastName = request.json[key]
            elif key == 'Email':
                student.Email = request.json[key]
        db.session.commit()

        return student_schema.dump(student), 200

#############################################
'''
INSTRUCTOR
'''
#############################################


@InstructorsNamespace.route('/createinstructor')
class instructorsResource(Resource):
    @api.expect(instructor)
    def post(self):

        new_instructor = Instructors()
        new_instructor.FirstName = request.json['FirstName']
        new_instructor.LastName = request.json['LastName']
        new_instructor.Email = request.json['Email']
        new_instructor.Password = generate_password_hash(request.json['Password'], method='sha256')

        instructor = Instructors.query.filter_by(Email=new_instructor.Email).first()
        if instructor:
            return "Email already taken", 400

        db.session.add(new_instructor)
        db.session.commit()
        return instructor_schema.dump(new_instructor), 201


@InstructorsNamespace.route('/<int:instructorID>')
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
@ResourceNamespace.route('/<int:courseID>/Resources')
class resourcesResource(Resource):
    def get(self,courseID):
        return

    def post(self,courseID):
        return

@ResourceNamespace.route('/<int:courseID>/resources/<int:resourceID>')
class resourceResource(Resource):
    def get(self,courseID,resourceID):
        return
    
    def delete(self,courseID,resourceID):
        return

@ResourceNamespace.route('/<int:courseID>/resources/<int:resourceID>/download')
class resourcesResourceOne(Resource):
    def get(self,courseID,resourceID):
        return

#############################################
'''
COURSE
'''
#############################################
@CourseNamespace.route('')
class coursesResource(Resource):
    def post(self):
        return

@CourseNamespace.route('/<int:courseID>')
class courseResource(Resource):
    def get(self,courseID):
        return
    
    def post(self,courseID):
        return
    
    def patch(self,courseID):
        return

@CourseNamespace.route('/<int:courseID>/student/<int:ids>')
class courseResourceOne(Resource):
    def get(self,courseID,ids):
        return
    
@CourseNamespace.route('/<int:courseID>/students')
class courseResourceTwo(Resource):
    def get(self,courseID):
        return

@CourseNamespace.route('/studentcourses')
class courseResourceThree(Resource):
    def get(self):
        return

@CourseNamespace.route('/studentcourses/<int:courseID>')
class courseResourceFour(Resource):
    def get(self,courseID):
        return

@CourseNamespace.route('/instructorcourses')
class courseResourceFive(Resource):
    def get(self):
        return
    
#############################################
'''
CLASSROOM
'''
#############################################

@ClassroomNamspace.route('/<int:courseID>/classrooms/<int:classroomID>')
class classroomResource(Resource):
    def get(self,courseID,classroomID):
        classRoom = VirtualClassrooms.query.get(classroomID)
        return json.dump(classRoom)
    
    def patch(self,courseID,classroomID):
        return

@ClassroomNamspace.route('/<int:courseID>/classrooms')
class classroomResourceOne(Resource):
    def get(self,courseID):
        classrooms = VirtualClassrooms.query.all()
        return {"Data": "Success"}
    
    # @api.expect(classroom)
    def post(self,courseID):
        new_classroom = VirtualClassrooms()
        new_classroom.ClassroomName = request.json['ClassroomName']
        new_classroom.CourseID = courseID
        new_classroom.URL = request.json['URL']

        db.session.add(new_classroom)
        db.session.commit()
        return json.dump(new_classroom)
    
@ClassroomNamspace.route('/<int:courseID>/classrooms/<int:classroomID>/join')
class classroomResourceTwo(Resource):
    def get(self,courseID,classroomID):
        return

if __name__ == "__main__":
    app.run(debug=True)