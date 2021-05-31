from flask_marshmallow import Marshmallow
from .models import *

ma = Marshmallow()


class StudentSchema(ma.Schema):
    class Meta:
        fields = ("FirstName","LastName","Email")

        model = Students

