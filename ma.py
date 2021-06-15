from flask_marshmallow import Marshmallow
from flask_sqlalchemy import model
from .models import *

ma = Marshmallow()


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
        model = Instructors
# class Resource(ma.Schema):
#     class Meta:
#         fields = ("FirstName","LastName","Email")
