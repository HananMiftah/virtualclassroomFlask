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
from VirtualClassroom import db
StudentNamespace = api.namespace("Student", path="/authenticate/students")

student_schema = StudentSchema()
students_schema = StudentSchema(many=True)

studentList_schema = StudentListSchema(many=True)


# Model required by flask_restplus for expect
student = api.model("Students", {
    'FirstName': fields.String(),
    'LastName': fields.String(),
    'Email': fields.String(),
    'Password': fields.String(),
})




@StudentNamespace.route('/createstudent')
class Student(Resource):
    @api.expect(student)
    def post(self):
        '''
        Create a new Student
        '''
        data = request.get_json()
        try:
            args = student_schema.load(data)
        except ValidationError as errors:
            return errors.messages , 400


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
    @jwt_required()
    def get(self,stuID):
        '''
        Get Student Info
        '''
        student = Students.query.filter_by(StudentID=stuID).first()

        if student:
            return student_schema.dump(student)
        return "Student not found",404
    @api.expect(student)
    @jwt_required()
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


@StudentNamespace.route('/studentByEmail/<string:email>')
class StudentByEmail(Resource):
    @jwt_required()
    def get(self,email):
        '''
        Get Student Info
        '''
        student = Students.query.filter_by(Email=email).first()
        print("SFNAME")
        print(student.FirstName)
        print("SFNAME")
        if student:
            return student_schema.dump(student)
        return abort(404, "Student not found")
