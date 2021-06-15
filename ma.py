from flask_marshmallow import Marshmallow
from flask_restplus import fields
from flask_restplus.inputs import email
from flask_sqlalchemy import model
from models import *

ma = Marshmallow()


class StudentSchema(ma.Schema):
    class Meta:
        order =True
        fields = ("FirstName","LastName","Email", "StudentID")
        model = Students

class InstructorSchema(ma.Schema):
    class Meta:
        fields = ("InstructorID","FirstName","LastName","Email")
        model = Instructors

# class ClassroomSchema(ma.Schema):
#     class Meta:
#         model = ClassroomStudents()
#         fields = ("FirstName","LastName","Email")

class CourseSchema(ma.Schema):
    class Meta:
        fields = ("CourseID","InstructorID","CourseTitle","CourseDescription")
        model = Courses

  


class ADDSTUDENT:
    CourseID=0
    email= ""
    name= ""

class AddStudentSchema(ma.Schema):
    class Meta:
        fields= ("CourseID","email","name")
        model = ADDSTUDENT
    


