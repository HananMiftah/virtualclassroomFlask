from virtualclassroomFlask.Resources import api
import re
from flask import Flask, request, flash
from flask_marshmallow import Marshmallow
from flask_restplus import Api, Resource, fields
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from virtualclassroomFlask.settings import *
from virtualclassroomFlask.models import *
from virtualclassroomFlask.ma import *
import json
#############################################
'''
CLASSROOM
'''
#############################################

ClassroomNamspace = api.namespace("Classroom", path="/courses")


@ClassroomNamspace.route('/<int:courseID>/classrooms/<int:classroomID>')
class classroomResource(Resource):
    def get(self,courseID,classroomID):
        classRoom = VirtualClassrooms.query.get(classroomID)
        return json.dump(classRoom)
    
    def patch(self,courseID,classroomID):
        return

@ClassroomNamspace.route('/<int:courseID>/classrooms')
class classroomResourceOne(Resource):
    def get(self,courseID):
        classrooms = VirtualClassrooms.query.all()
        return {"Data": "Success"}
    
    @api.expect(classroom)
    def post(self,courseID):
        new_classroom = VirtualClassrooms()
        new_classroom.ClassroomName = request.json['ClassroomName']
        new_classroom.CourseID = courseID
        new_classroom.URL = request.json['URL']

        db.session.add(new_classroom)
        db.session.commit()
        return json.dump(new_classroom)
    
@ClassroomNamspace.route('/<int:courseID>/classrooms/<int:classroomID>/join')
class classroomResourceTwo(Resource):
    def get(self,courseID,classroomID):
        return