# from ma import AddStudentSchema
import re
# from virtualclassroomFlask.models import Instructors
# from virtualclassroomFlask.application import Student
from flask import Flask, request, flash
from flask_marshmallow import Marshmallow
from flask_restplus import Resource, fields,reqparse,abort
from werkzeug.security import generate_password_hash, check_password_hash

from VirtualClassroom.Resources import api
from VirtualClassroom.schemas import *
from VirtualClassroom.models import *
from flask_jwt_extended import ( create_access_token, get_jwt,
                            jwt_required, get_jwt_identity)
from datetime import timedelta
from VirtualClassroom import db

CourseNamespace = api.namespace("Course", path="/courses")


add_student_schema = AddStudentSchema()

studentList_schema = StudentListSchema()
studentLists_schema = StudentListSchema(many=True)

course_schema = CourseSchema()
courses_schema = CourseSchema(many=True)

courseStudents = api.model("CourseStudents",{
    'CourseID': fields.Integer(),
    'StudentID': fields.Integer()
})
course = api.model("Courses", {
    'InstructorID': fields.Integer(),
    'CourseTitle': fields.String(),
    'CourseDescription': fields.String(),
    
})



@CourseNamespace.route('')
class coursesResource(Resource):
    @jwt_required()
    @api.expect(course)
    @jwt_required()
    def post(self):
       new_course = Courses()
       new_course.InstructorID = request.json['InstructorID']
       new_course.CourseTitle = request.json['CourseTitle']
       new_course.CourseDescription = request.json['CourseDescription']

       db.session.add(new_course)

    
       db.session.commit()
       print(new_course)
       return course_schema.dump(new_course),201
       


@CourseNamespace.route('/<int:courseID>/student/<int:studentID>')
class deleteStudent(Resource):
    @jwt_required()
    def delete(self,courseID,studentID):
        c = CourseStudents.query.filter_by(StudentID=studentID, CourseID=courseID).first()
        if not c:
            return 'Student Not Registered in this course', 400
            
        db.session.delete(c)
        db.session.commit()


@CourseNamespace.route('/<int:courseID>')

class courseResource(Resource):
    @jwt_required()
    def get(self,courseID):
        print
        result = Courses.query.filter_by(CourseID=courseID).first()
        print(result)
        if not result:
            return "Course Not Found", 404

        return course_schema.dump(result)
    
    @api.expect(courseStudents)
    @jwt_required()
    def post(self,courseID):
        print()
        student = CourseStudents.query.filter_by(StudentID = request.json['StudentID'], CourseID= courseID).first()
        if student:
            abort(400, message="Student Already Registered")
        
        add_student = CourseStudents()
        add_student.CourseID = request.json['CourseID']
        add_student.StudentID = request.json['StudentID']

        db.session.add(add_student)
        db.session.commit()
        print("COMMIT")
        stu=ADDSTUDENT()
        stu.CourseID=add_student.CourseID
        print(Students.query.filter_by(StudentID=add_student.StudentID).first())
        stu.email = Students.query.filter_by(StudentID=add_student.StudentID).first().Email
        stu.name = Students.query.filter_by(StudentID=add_student.StudentID).first().FirstName +" "+ Students.query.filter_by(StudentID=add_student.StudentID).first().LastName
        return add_student_schema.dump(stu), 200
    
@CourseNamespace.route('/student/<int:courseID>')
class courseResourceOne(Resource):
    @jwt_required()
    def get(self,courseID):
        studentID = get_jwt_identity()
        course = Courses.query.filter_by(CourseID= courseID).first()
        if not course:
            return "Course Not Found", 404


        c = CourseStudents.query.filter_by(StudentID=studentID, CourseID=courseID).first()
        if not c:
            return 'You are not registered to this course', 400
            
        return course_schema.dump(course)

    
    # LIST OF STUDENTS IN A COURSE
@CourseNamespace.route('/<int:courseID>/students')
class courseResourceTwo(Resource):
    @jwt_required()
    def get(self,courseID):
        courses = CourseStudents.query.filter_by(CourseID = courseID).all()
        students=[]
        for course in courses:
            student = StudentListSchema()
            s = Students.query.filter_by(StudentID = course.StudentID).first()
            student.name= s.FirstName + " " + s.LastName
            student.email = s.Email
            student.id = s.StudentID
            students.append(student)


        # TODO : Create Schema
        return studentLists_schema.dump(students)

    # def post(self,courseID):

    #     return 
# A STUDENTS LIST OF COURSES
@CourseNamespace.route('/studentcourses')
class courseResourceThree(Resource):
    @jwt_required()
    def get(self):
        # TODO fetch real student Id
        student_id = get_jwt_identity()
        courses= CourseStudents.query.filter_by(StudentID=student_id).all()
        lst =[]

        for course in courses:
            a= COURSES()
            c = Courses.query.filter_by(CourseID = course.CourseID).first()
            a.CourseId = course.CourseID
            a.CourseTitle = c.CourseTitle
            a.CourseDescription = c.CourseDescription
            a.InstructorID = c.InstructorID
            lst.append(a)

        return courses_schema.dump(lst)

@CourseNamespace.route('/studentcourses/<int:courseID>')
class courseResourceFour(Resource):
    @jwt_required()
    def get(self,courseID):
        # TODO fetch real student Id
        student_id = get_jwt_identity()
        course= CourseStudents.query.filter_by(StudentID=student_id, CourseID=courseID).first()
        if course:
            return Courses.query.filter_by(courseID = courseID).first()
        return abort(404, 'Student Not enrolled')

@CourseNamespace.route('/instructorcourses')
class courseResourceFive(Resource):
    @jwt_required()
    def get(self):
        instructor_id = get_jwt_identity()
        print("Instructor ID" + str(instructor_id))
        courses= Courses.query.filter_by(InstructorID=instructor_id).all()
        lst =[]

        for course in courses:
            a= COURSES()
            print("SOME COURSE")
            print(course.CourseID)
            c = Courses.query.get(course.CourseID)
            a.CourseID = course.CourseID
            a.CourseTitle = c.CourseTitle
            a.CourseDescription = c.CourseDescription
            a.InstructorID = c.InstructorID
            lst.append(a)
        return courses_schema.dump(lst)
    