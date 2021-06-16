
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
import os

ResourceNamespace = api.namespace("Resource", path="/courses")

resource_schema = ResourceSchema()







@ResourceNamespace.route('/<int:courseID>/resources')
class resourcesResource(Resource):
    def post(self,courseID):
        # saving the file to the server
        fileType = request.headers['Content-Type'].split("/")[1]
        contentType = request.headers['Content-Type']
        fileName = request.headers['File-Name'] #TODO

        randomfileName = str(uuid.uuid4())
        with open(os.path.join(upload_folder, randomfileName+"."+fileType), "wb") as fp:
            fp.write(request.data)

        # saving the file's metadata to database
        new_resource = Resources()
        new_resource.FilePath = upload_folder
        new_resource.FileName = fileName +"."+ fileType
        new_resource.RandomFileName = randomfileName +"."+ fileType
        new_resource.ContentType = contentType
        new_resource.CourseID = int(courseID)
        new_resource.CreationDate = datetime.now()

        db.session.add(new_resource)
        db.session.commit()
        
        return {'resourceID':new_resource.ResourceID}, 201

@ResourceNamespace.route('/<int:courseID>/resources/<int:resourceID>')
class resourceResource(Resource):
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
    def get(self,courseID,resourceID):
        file = Resources.query.filter_by(ResourceID=int(resourceID)).first()
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
