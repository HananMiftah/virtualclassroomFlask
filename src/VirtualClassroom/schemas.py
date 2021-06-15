from marshmallow import fields, Schema, validate, validates, ValidationError
from models import *
from flask_sqlalchemy import model
from . import ma

from .models import *


class StudentSchema(ma.Schema):
    class Meta:
        fields = ("FirstName","LastName","Email", "StudentID")
        model = Students
        ordered=True
    StudentID=fields.Integer(data_key="userid")
    FirstName = fields.String(required=True)
    LastName = fields.String(required=True)
    Email = fields.Email(required=True)
    
    @validates("Email")
    def validate_username(self, username):
        if bool(Students.query.filter_by(Email=Email).first()):
            raise ValidationError(
                '"{username}" Email already exists, '
                'please use a different username.'.format(Email=Email)
            )


class InstructorSchema(ma.Schema):
    class Meta:
        fields = ("FirstName","LastName","Email")
        model = Instructors
    InstructorID=fields.Integer(data_key="userid")
    FirstName = fields.String(required=True)
    LastName = fields.String(required=True)
    Email = fields.Email(required=True)
    
    @validates("Email")
    def validate_username(self, username):
        if bool(Instructors.query.filter_by(Email=Email).first()):
            raise ValidationError(
                '"{username}" Email already exists, '
                'please use a different username.'.format(Email=Email)
            )
# class ClassroomSchema(ma.Schema):
#     class Meta:
#         model = ClassroomStudents()
#         fields = ("FirstName","LastName","Email")

class CourseSchema(ma.Schema):
    class Meta:

        fields = ("CourseID","InstructorID","CourseTitle","CourseDescription")
        model = Courses
# class Resource(ma.Schema):
#     class Meta:
#         fields = ("FirstName","LastName","Email")
