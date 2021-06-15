import re
from flask import Flask, request, flash
from flask_marshmallow import Marshmallow
from flask_restplus import Api, Resource, fields, abort
from flask_cors import CORS
from marshmallow import ValidationError
from flask_jwt_extended import (get_jwt_identity)


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

AuthenticationNamespace = api.namespace("Authentication", path="/api/authenticate")
StudentNamespace = api.namespace("Student", path="/api/authenticate/students")
InstructorsNamespace = api.namespace("Instructor", path="/api/authenticate/instructors")
ClassroomNamspace = api.namespace("Classroom", path="/api/courses")
ResourceNamespace = api.namespace("Resource", path="/api/courses")
CourseNamespace = api.namespace("Course", path="/api/courses")


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


# Model required by flask_restplus for expect
course = api.model("Courses", {
    'InstructorID': fields.Integer(),
    'CourseTitle': fields.String(),
    'CourseDescription': fields.String(),
    
})


courseStudents = api.model("CourseStudents",{
    'CourseID': fields.Integer(),
    'StudentID': fields.Integer()
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
    def post(self):
        return 


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
    @api.expect(course)
    def post(self):
       args = request.json()
       new_course = Courses()
       new_course.InstructorID = args['InstructorId']
       new_course.CourseTitle = args['CourseTitle']
       new_course.CourseDescription = args['CourseDescription']

       db.session.add(new_course)

       db.commit()

       return course_schema.dump(new_course), 201
       
       

@CourseNamespace.route('/<int:courseID>')
class courseResource(Resource):
    def get(self,courseID):
        result = Courses.query.filter_by(CourseID=courseID).first()

        if not result:
            abort(404, message="Course Not Found")

        return course_schema.dump(result)
    
    @api.expect(courseStudents)
    def post(self,courseID):
        args = request.json()
        student = CourseStudents.query.filter_by(StudentID = args['StudentID']).first()
        if student:
            abort(400, message="Student Already Registered")
        
        add_student = CourseStudents()
        add_student.CourseID = courseID
        add_student.StudentID = args['StudentID']

        db.session.add(add_student)
        db.commit()

        # TODO    
        return "", 200
    
    def patch(self,courseID):
        return

@CourseNamespace.route('/student/<int:courseId>')
class courseResourceOne(Resource):
    def get(self,courseID):
        args = request.json()
        student = CourseStudents.query.filter_by(StudentID = args['StudentID']).first()
        if student:
            abort(400, message="Student Already Registered")
        
        add_student = CourseStudents()
        add_student.CourseID = courseID
        add_student.StudentID = args['StudentID']

        db.session.add(add_student)
        db.commit()
                
        return "", 200

    
@CourseNamespace.route('/<int:courseID>/students')
class courseResourceTwo(Resource):
    def get(self,courseID):
        students = CourseStudents.query.filter_by(courseID = courseID).all()

        # TODO : Create Schema
        return students

    # def post(self,courseID):

    #     return 

@CourseNamespace.route('/studentcourses')
class courseResourceThree(Resource):
    def get(self):
        # TODO fetch real student Id
        studentId = get_jwt_identity()
        courseIdlst = CourseStudents.query.filter_by(StudentID = studentId).all()
        print(courseIdlst)

        return courseIdlst

@CourseNamespace.route('/studentcourses/<int:courseID>')
class courseResourceFour(Resource):
    def get(self,courseID):
        # TODO fetch real student Id
        student_id = get_jwt_identity()
        course= CourseStudents.query.filter_by(StudentID=student_id, CourseID=courseID).first()
        if course:
            return Courses.query.filter_by(courseID = courseID).first()
        return abort(404, 'Student Not enrolled')

@CourseNamespace.route('/instructorcourses')
class courseResourceFive(Resource):
    def get(self):
        # TODO fetch real instructor Id
        instructorId = get_jwt_identity()

        courseLst = Courses(InstructorID = instructorId).all()

        # TODO create Schema
        return courseLst
    
#############################################
'''
CLASSROOM
'''
#############################################

@ClassroomNamspace.route('/<int:courseID>/classrooms/<int:classroomID>')
class classroomResource(Resource):
    def get(self,courseID,classroomID):
        return
    
    def patch(self,courseID,classroomID):
        return

@ClassroomNamspace.route('/<int:courseID>/classrooms')
class classroomResourceOne(Resource):
    def get(self,courseID):
        return
    
    def post(self,courseID):
        return
    
@ClassroomNamspace.route('/<int:courseID>/classrooms/<int:classroomID>/join')
class classroomResourceTwo(Resource):
    def get(self,courseID,classroomID):
        return

if __name__ == "__main__":
    app.run(debug=True)