from flask import Flask, request
from flask_marshmallow import Marshmallow
from flask_restplus import Api, Resource, fields
from flask_cors import CORS

from settings import *
from models import *
from ma import *


app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS


db.init_app(app)
ma = Marshmallow(app)

api = Api(app, version='1.0', title='Virtual Classroom API',
          description='A simple Virtual Classroom API')


student_schema = StudentSchema()
students_schema = StudentSchema(many=True)



# Model required by flask_restplus for expect
student = api.model("Students", {
    'FirstName': fields.String(),
    'LastName': fields.String(),
    'Email': fields.String(),
})


@api.route('/api/authenticate/students')
# @cross_origin()
class studentResource(Resource):
    def get(self):
        '''
        Get Students Info
        '''
        students = Students.query.all()
        print(students)
        return students_schema.dump(students)


    
