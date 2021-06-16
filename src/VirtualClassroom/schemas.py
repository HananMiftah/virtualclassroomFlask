# from typing_extensions import Required
from marshmallow import fields, Schema, validate, validates, ValidationError
from flask_sqlalchemy import model
from . import ma

from .models import *


class StudentSchema(ma.Schema):
    class Meta:
        ordered =True
        fields = ("FirstName","LastName","Email", "StudentID","Password")
        model = Students
    StudentID=fields.Integer(data_key="userid")
    FirstName = fields.String(required=True)
    LastName = fields.String(required=True)
    Email = fields.Email(required=True)
    Password = fields.String(required=True, load_only=True)

    
    
    @validates("Email")
    def validate_username(self, Email):
        if bool(Students.query.filter_by(Email=Email).first() or Instructors.query.filter_by(Email=Email).first() ):
            raise ValidationError(
                '"{Email}" Email already exists, '
                'please use a different username.'.format(Email=Email)
            )


class InstructorSchema(ma.Schema):
    class Meta:
        fields = ("InstructorID","FirstName","LastName","Email","Password")
        model = Instructors
        ordered=True
    InstructorID=fields.Integer(data_key="userid")
    FirstName = fields.String(required=True)
    LastName = fields.String(required=True)
    Email = fields.Email(required=True)
    Password = fields.String(required=True, load_only=True, data_key="Password")
    
    @validates("Email")
    def validate_username(self, Email):
        if bool(Instructors.query.filter_by(Email=Email).first() or Students.query.filter_by(Email=Email).first()):
            raise ValidationError(
                '"{Email}" Email already exists, '
                'please use a different username.'.format(Email=Email)
            )
# class ClassroomSchema(ma.Schema):
#     class Meta:
#         model = ClassroomStudents()
#         fields = ("FirstName","LastName","Email")


class COURSES:
    CourseID=0
    InstructorID=0
    CourseTitle=""
    CourseDescription=""




class STUDENTLIST:
    name=""
    id=0
    email=""


class CourseSchema(ma.Schema):
    class Meta:
        fields = ("CourseID","InstructorID","CourseTitle","CourseDescription")
        model = COURSES
    CourseID=fields.Integer(data_key="userid")
    FirstName = fields.String(required=True)
    LastName = fields.String(required=True)
    Email = fields.Email(required=True)

  
class ADDSTUDENT:
    CourseID=0
    email= ""
    name= ""
  

class AddStudentSchema(ma.Schema):
    class Meta:
        fields= ("CourseID","email","name")
        model = ADDSTUDENT
    CourseId=fields.Integer(Required=True,data_key="userid")
    name = fields.String(required=True)
    email = fields.Email(required=True)
    


class StudentListSchema(ma.Schema):
    class Meta:
        fields =("name","id","email")
        model=STUDENTLIST
    id=fields.Integer(Required=True,data_key="userid")
    name = fields.String(required=True)
    name = fields.Email(required=True)


class ClassroomSchema(ma.Schema):
    class Meta:
        fields =("ClassroomName","Date","StartTime","EndTime","CourseID","ClassroomID")
        model=VirtualClassrooms

class ClassroomStudentSchema(ma.Schema):
    class Meta:
        fields =("name","id","email")
        model=STUDENTLIST


class ResourceSchema(ma.Schema):
    class Meta:
        fields = ("ResourceID", "FileName", "CreationDate")
        model = Resources