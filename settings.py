# Flask settings
FLASK_SERVER_NAME = 'localhost:8888'
FLASK_DEBUG = True  # Do not use debug mode in production
UPLOAD_FOLDER = './Resources/static/resources'

# SQLAlchemy settings
SQLALCHEMY_DATABASE_URI = 'postgresql://xgkqkevc:64RJl4BfrwdyN7R_fhCI6ZdKERgfLFSY@batyr.db.elephantsql.com/xgkqkevc'
# SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:hanan@localhost/virtualclassdb'
SQLALCHEMY_TRACK_MODIFICATIONS = False
