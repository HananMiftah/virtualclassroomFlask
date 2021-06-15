from marshmallow import fields, Schema, validate, validates, ValidationError
from flask_sqlalchemy import model
from . import ma

from .models import *


class StudentSchema(ma.Schema):
    class Meta:
        ordered =True
        fields = ("FirstName","LastName","Email", "StudentID")
        model = Students
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
        fields = ("InstructorID","FirstName","LastName","Email")
        model = Instructors
        ordered=True
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
    


class StudentListSchema(ma.Schema):
    class Meta:
        fields =("name","id","email")
        model=STUDENTLIST

class COURSES:
    CourseID=0
    InstructorID=0
    CourseTitle=""
    CourseDescription=""




class STUDENTLIST:
    name=""
    id=0
    email=""
