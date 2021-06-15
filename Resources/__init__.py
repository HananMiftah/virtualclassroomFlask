import re
from flask import Flask, request, flash
from flask_marshmallow import Marshmallow
from flask_restplus import Api, Resource, fields
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from virtualclassroomFlask.settings import *
from virtualclassroomFlask.models import *
from virtualclassroomFlask.ma import *
import json



blueprint = Blueprint('api_v1', __name__)
api = Api(blueprint, version='1.0', title='Virtual Classroom API',
          description='A simple Virtual Classroom API')
# api.add_resource(Classroom, "/courses")
AuthenticationNamespace = api.namespace("Authentication", path="/authenticate")
StudentNamespace = api.namespace("Student", path="/authenticate/students")
InstructorsNamespace = api.namespace("Instructor", path="/authenticate/instructors")
ResourceNamespace = api.namespace("Resource", path="/courses")
CourseNamespace = api.namespace("Course", path="/courses")


student_schema = StudentSchema()
students_schema = StudentSchema(many=True)

course_schema = CourseSchema()
course_schema = CourseSchema(many=True)


# Model required by flask_restplus for expect
student = api.model("Students", {
    'FirstName': fields.String(),
    'LastName': fields.String(),
    'Email': fields.String(),
    'Password': fields.String(),
})

classroom = api.model("VirualClassrooms", {
    'ClassroomName': fields.String(),
    'URL': fields.String() 
})
#TODO
course = api.model("Courses", {

})

instrucor = api.model("Instructors", {
    "FirstName": fields.String(),
    "LastName":fields.String(),
    "Email": fields.String(),
    "Password": fields.String() 
})

#############################################
'''
AUTHENTICATION
'''
#############################################

@AuthenticationNamespace.route('')
# @cross_origin()
class authentication(Resource):
    def get(self):
        return 

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
    def get(self,stuID):
        '''
        Get Student Info
        '''
        student = Students.query.filter_by(StudentID=stuID).first()

        if student:
            return student_schema.dump(student)
        return "Student not found",404
    @api.expect
    def patch(self,stuID):
        '''
        Edit Student Info
        '''
        student = Students.query.filter_by(StudentID=stuID).first()

        return

@StudentNamespace.route('/studentbyemail')
class studentsResources(Resource):
    def get(self):
        return

@StudentNamespace.route('/studentbyemail/<int:studentEmail>')
class studentsResourcesOne(Resource):
    def get(self,studentEmail):
        '''
        Get Student Info Using Email
        '''

        return

#############################################
'''
INSTRUCTOR
'''
#############################################

@InstructorsNamespace.route('')
class instructorsResource(Resource):
    def get(self):
        return

@InstructorsNamespace.route('/createinstructor')
class instructorsResource(Resource):
    @api.expect(instrucor)
    def post(self):
        new_instructor = Instructors()
        new_instructor.Email = request.json['Email']
        new_instructor.FirstName = request.json["FirstName"]
        new_instructor.LastName = request.json["LastName"]
        new_instructor.Password = generate_password_hash(request.json['Password'], method='sha256')

        db.session.add(new_instructor)
        db.session.commit()
        return json.dumps({"data": True})


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

def create_app():
    from virtualclassroomFlask.Resources import ClassroomNamspace
    app = Flask(__name__)
    app.register_blueprint(api, url_prefix='/api')

    CORS(app)

    db_uri = SQLALCHEMY_DATABASE_URI
    if db_uri.startswith("postgres://"):
        db_uri = db_uri.replace("postgres://", "postgresql://", 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
    app.debug = True

    db.init_app(app)
    ma = Marshmallow(app)

    return app



if __name__ == "__main__":
    app.run(debug=True)