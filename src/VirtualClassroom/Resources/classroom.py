import re
from flask import Flask, request, flash
from flask_marshmallow import Marshmallow
from flask_restplus import Api, Resource, fields
from werkzeug.security import generate_password_hash, check_password_hash

from VirtualClassroom.Resources import api
from VirtualClassroom.schemas import *
from VirtualClassroom.models import *
#############################################
'''
CLASSROOM
'''
#############################################

ClassroomNamspace = api.namespace("Classroom", path="/courses")

classroom = api.model("VirualClassrooms", {
    'ClassroomName': fields.String(),
    'URL': fields.String() 
})

@ClassroomNamspace.route('/<int:courseID>/classrooms/<int:classroomID>')
class classroomResource(Resource):
    def get(self,courseID,classroomID):
        classRoom = VirtualClassrooms.query.get(classroomID)
        return json.dumps(classRoom)
    
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
