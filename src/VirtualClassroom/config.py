class Config:
    # SQLALCHEMY_DATABASE_URI = 'postgresql://xgkqkevc:64RJl4BfrwdyN7R_fhCI6ZdKERgfLFSY@batyr.db.elephantsql.com/xgkqkevc'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:root@localhost/virtualclassdb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = '5791628bb0b13ce0c676dfde280ba245'
    JWT_SECRET_KEY = '5791628bb0b13ce0c676dfde280ba245'
    JWT_BLACKLIST_ENABLED = ['access']
    UPLOAD_FOLDER = './../../static'
