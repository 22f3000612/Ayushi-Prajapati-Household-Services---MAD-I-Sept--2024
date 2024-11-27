#Starting of the Application
from flask import Flask
from Backend.models import db
app=None

def setup_app():
    app=Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///CareConnect.sqlite3"
    app.config['UPLOAD_FOLDER'] = 'static/uploads/'
    db.init_app(app)          #Flask app connected to db
    app.app_context().push()  #Direct access to other modules
    app.debug=True
    print("CareConnect App is started")

#call setup
setup_app()

    

from Backend.controllers import *

if __name__ == "__main__":
    app.run()