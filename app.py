#Starting of the Application
from flask import Flask,render_template
from flask_migrate import Migrate
from Backend.models import db

app=None

def setup_app():
    app=Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///CareConnect.sqlite3"
    app.config['UPLOAD_FOLDER'] = 'static/uploads/'
    app.config['SECRET_KEY'] = 'ALL SECRET'
    db.init_app(app)          #Flask app connected to db
    app.app_context().push()  #Direct access to other modules
    app.debug=True
    migrate = Migrate(app,db)
    print("CareConnect App is started")

#call setup
setup_app()

    

from Backend.controllers import *

if __name__ == "__main__":
    app.run()