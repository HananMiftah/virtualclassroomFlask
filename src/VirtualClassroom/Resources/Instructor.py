import re
# from virtualclassroomFlask.models import Instructors
# from virtualclassroomFlask.application import Student
from marshmallow import fields, Schema, validate, validates, ValidationError
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


InstructorsNamespace = api.namespace("Instructor", path="/authenticate/instructors")




instructor_schema = InstructorSchema()
instructors_schema = InstructorSchema(many=True)

instructor = api.model("Instructors", {
    'FirstName': fields.String(),
    'LastName': fields.String(),
    'Email': fields.String(),
    'Password': fields.String(),
})



@InstructorsNamespace.route('/createinstructor')
class instructorsResource(Resource):
    def post(self):

        data = request.get_json()
        try:
            args = instructor_schema.load(data)
        except ValidationError as errors:
            return errors.messages , 400

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
    @jwt_required()
    def get(self,instructorID):
        instructor = Instructors.query.filter_by(StudentID=instructorID).first()

        if instructor:
            return student_schema.dump(instructor)
        return "Instructor not found",404
        
    @jwt_required()
    def patch(self,instructorID):
        return

