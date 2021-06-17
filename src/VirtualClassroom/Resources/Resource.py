
import re
# from settings import UPLOAD_FOLDER
# from virtualclassroomFlask.models import Instructors
# from virtualclassroomFlask.application import Student
from marshmallow import fields, Schema, validate, validates, ValidationError
from flask import Flask, request, flash, make_response
from flask_marshmallow import Marshmallow
from flask_restplus import Resource, fields,reqparse,abort
from werkzeug.security import generate_password_hash, check_password_hash

from src.VirtualClassroom.Resources import api
from src.VirtualClassroom.schemas import *
from src.VirtualClassroom.models import *
from src.VirtualClassroom.config import *

from flask_jwt_extended import ( create_access_token, get_jwt,
                            jwt_required, get_jwt_identity)
from datetime import timedelta
from src.VirtualClassroom import db
import os,uuid


ResourceNamespace = api.namespace("Resource", path="/course")

resource_schema = ResourceSchema()
resources_schema = ResourceSchema(many=True)

upload_folder = 'static'





@ResourceNamespace.route('/<int:courseID>/resources')
class resourcesResource(Resource):

    @jwt_required()
    def post(self,courseID):
        # saving the file to the server
        contentType = request.headers['Content-Type']

        randomfileName = str(uuid.uuid4())
        with open(os.path.join(upload_folder, randomfileName), "wb") as fp:
            fp.write(request.files['file'].stream.read())

        # saving the file's metadata to database
        new_resource = Resources()
        new_resource.FilePath = upload_folder
        new_resource.FileName = request.files['file'].filename
        new_resource.RandomFileName = randomfileName
        new_resource.ContentType = contentType
        new_resource.CourseID = int(courseID)
        new_resource.CreationDate = datetime.now()

        db.session.add(new_resource)
        db.session.commit()
        
        return {'resourceID':new_resource.ResourceID}, 201
    @jwt_required()
    def get(self,courseID):
        file = Resources.query.filter_by(CourseID=courseID).all()
        if file:
            return resources_schema.dump(file), 200
        return [], 200

@ResourceNamespace.route('/<int:courseID>/resources/<int:resourceID>')
class resourceResource(Resource):
    @jwt_required()

    def get(self,courseID,resourceID):
        file = Resources.query.filter_by(ResourceID=int(resourceID)).first()
        if file:
            return resource_schema.dump(file), 200
        return 'Resource not found', 404
    
    def delete(self,courseID,resourceID):
        file = Resources.query.filter_by(ResourceID=int(resourceID)).first()
        if file:
            db.session.delete(file)
            db.session.commit()
            return 'Deleted Succesfully',200
        return {"message": "File not found"}, 404

@ResourceNamespace.route('/<int:courseID>/resources/<int:resourceID>/download')
class resourcesResourceOne(Resource):
    @jwt_required()
    def get(self,courseID,resourceID):
        file = Resources.query.filter_by(ResourceID=int(resourceID)).first()
        print(file.FileName)
        if file:
            try:
                filePath = file.FilePath
                randomFileName = file.RandomFileName
                fileContent = None

                with open(os.path.join(filePath, randomFileName), "rb") as fp:
                    fileContent = fp.read()
                response = make_response(fileContent)
                response.headers.set('Content-Type', file.ContentType)
                return response
            except:
                return 'Resource not found', 404
            
        
        return 'Resource not found', 404
