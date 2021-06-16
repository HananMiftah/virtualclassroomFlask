import re
# from virtualclassroomFlask.models import Instructors
# from virtualclassroomFlask.application import Student
from flask import Flask, request, flash
from marshmallow import fields, Schema, validate, validates, ValidationError

from flask_marshmallow import Marshmallow
from flask_restplus import Resource, fields,reqparse,abort
from werkzeug.security import generate_password_hash, check_password_hash

from VirtualClassroom.Resources import api
from VirtualClassroom.schemas import *
from VirtualClassroom.models import *
from flask_jwt_extended import ( create_access_token, get_jwt,
                            jwt_required, get_jwt_identity)
from datetime import timedelta
from dateutil.parser import parse

from VirtualClassroom import db


ClassroomNamspace = api.namespace("Classroom", path="/courses")
classroom_schema = ClassroomSchema()
classrooms_schema = ClassroomSchema(many=True)

studentList_schema = StudentListSchema(many=True)

classroom = api.model("Virtualclassrooms",{
    'ClassroomName': fields.String(),
    'Date': fields.String(),
    'StartTime': fields.String(),
    'EndTime': fields.String()
})

@ClassroomNamspace.route('/<int:courseID>/classrooms/<int:classroomID>')
class classroomResource(Resource):
    @jwt_required()
    def get(self,courseID,classroomID):
        classroom = VirtualClassrooms.query.filter_by(ClassroomID=classroomID, CourseID=courseID).first()
        if not classroom:
            return "Classroom Not Found", 404
        return classroom_schema.dump(classroom), 200
    @jwt_required()
    def delete(self,courseID,classroomID):
        classroom = VirtualClassrooms.query.filter_by(ClassroomID=classroomID, CourseID=courseID).first()
        if not classroom:
            return "Classroom not found", 404
        db.session.delete(classroom)
        db.session.commit()
        return "Successfully deleted",204

@ClassroomNamspace.route('/<int:courseID>/classrooms/<int:classroomID>/attendance')
class classroomResource(Resource):
    @jwt_required()
    def get(self,courseID,classroomID):
        classroom = VirtualClassrooms.query.filter_by(ClassroomID=classroomID, CourseID=courseID).first()
        if not classroom:
            return "Classroom Not Found", 404
        class_stu = ClassroomStudents.query.filter_by(ClassroomID=classroomID).all()
        students=[]
        for stu in class_stu:
            student = StudentListSchema()
            s = Students.query.filter_by(StudentID = stu.StudentID).first()
            student.name= s.FirstName + " " + s.LastName
            student.email = s.Email
            student.id = s.StudentID
            students.append(student)


        return studentList_schema.dump(students)
    

@ClassroomNamspace.route('/<int:courseID>/classrooms')
class classroomResourceOne(Resource):
    @jwt_required()
    def get(self,courseID):
        classrooms = VirtualClassrooms.query.filter_by(CourseID=courseID)
        if not classrooms:
            return "No classrooms available"
        return classrooms_schema.dump(classrooms), 200
    
    @api.expect(classroom)
    @jwt_required()
    def post(self,courseID):
        new_classroom = VirtualClassrooms()
        new_classroom.ClassroomName = request.json['ClassroomName']
        new_classroom.CourseID = courseID
        # new_classroom.URL = "url"
        print("\n")
        print(request.json['Date'])
        new_classroom.Date = datetime.strptime(request.json['Date'],'%Y-%m-%dT%H:%M:%S.%fZ')
        new_classroom.StartTime = request.json['StartTime']
        new_classroom.EndTime = request.json['EndTime']

        db.session.add(new_classroom)
        db.session.commit()
        return classroom_schema.dump(new_classroom),201
    
@ClassroomNamspace.route('/<int:courseID>/classrooms/<int:classroomID>/join')
class classroomResourceTwo(Resource):
    @jwt_required()
    def get(self,courseID,classroomID):
        return