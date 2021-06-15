import re
# from virtualclassroomFlask.models import Instructors
# from virtualclassroomFlask.application import Student
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


AuthenticationNamespace = api.namespace("Authentication", path="/api/authenticate")

user_auth_arguments = reqparse.RequestParser()
user_auth_arguments.add_argument('username', type=str, help="Username", required=True)
user_auth_arguments.add_argument('password', type=str, help="Password", required=True)

userCred = api.model("UserCred", {
    'UserName': fields.String(),
    'Password': fields.String() 
})

@AuthenticationNamespace.route('')
# @cross_origin()

class authentication(Resource):
    @api.expect(userCred)
    def post(self):
        args = user_auth_arguments.parse_args()
        username = args['username']
        password = args['password']
        user=Student.query.filter_by(Email=username).first()
        role="Student"
        if user and  check_password_hash(user.Password , password):
            expires = timedelta(days=30)
            additional_claims = {"role": role}
            token = create_access_token(
                identity=user.id, 
                expires_delta=expires,
                additional_claims=additional_claims)
            return {'token': token}
        user=Instructors.query.filter_by(Email=username).first()
        role="Instrucotr"
        if user and  check_password_hash(user.Password , password):
            expires = timedelta(days=30)
            additional_claims = {"role": role}
            token = create_access_token(
                identity=user.id, 
                expires_delta=expires,
                additional_claims=additional_claims)
            return {'token': token}
        return abort(401, message="Incorrect Username or password")


         