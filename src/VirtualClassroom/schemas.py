from flask_marshmallow import Marshmallow
from flask_sqlalchemy import model
from . import ma

from .models import *


class StudentSchema(ma.Schema):
    class Meta:
        fields = ("FirstName","LastName","Email", "StudentID")
        model = Students

class InstructorSchema(ma.Schema):
    class Meta:
        fields = ("FirstName","LastName","Email")
        model = Instructors

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
