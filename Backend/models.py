#Data Models
from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

#Entity 1
class Admin(db.Model):
    __tablename__="Admin"
    email=db.Column(db.String,unique=True,nullable=False,primary_key=True)
    password=db.Column(db.String,nullable=False)


#Entity 2
class Customer(db.Model):
    __tablename__="Customer"
    id = db.Column(db.Integer, primary_key=True)
    email=db.Column(db.String,unique=True,nullable=False)
    password=db.Column(db.String,nullable=False)
    contact_number=db.Column(db.Integer,nullable=False)
    fullname =db.Column(db.String,nullable=False)
    address =db.Column(db.String,nullable=False)
    pincode=db.Column(db.Integer,nullable=False)
    status=db.Column(db.String,default="Active")
    
    

    
#Entity 3
class Professional(db.Model):
    __tablename__="Professional"
    id = db.Column(db.Integer, primary_key=True)
    email=db.Column(db.String,unique=True,nullable=False)
    password=db.Column(db.String,nullable=False)
    fullname=db.Column(db.String,nullable=False)
    contact_number=db.Column(db.Integer,nullable=False)
    address=db.Column(db.String,nullable=False)
    pincode=db.Column(db.Integer,nullable=False)   
    experience=db.Column(db.String,nullable=False)
    professional_summary=db.Column(db.String,nullable=False)
    service_name=db.Column(db.String,nullable=False)
    status=db.Column(db.String,default="Active")
    p_req=db.Column(db.String,default="Pending")
    
    
    
#Entity 4
class Service(db.Model):
    __tablename__="Service"
    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String,nullable=False)
    description=db.Column(db.String,nullable=False)
    baseprice=db.Column(db.Integer,default=0.0)
    subservice=db.Column(db.String,nullable=False)
    location=db.Column(db.String,nullable=False)
    pincode=db.Column(db.String,nullable=False)

#Entity 5
class Servicereq(db.Model):
    __tablename__="Servicereq"
    id = db.Column(db.Integer, primary_key=True)
    Professional_id=db.Column(db.Integer, db.ForeignKey("Professional.id"),nullable=True)
    Service_id=db.Column(db.Integer, db.ForeignKey("Service.id"),nullable=False)
    Customer_id=db.Column(db.Integer, db.ForeignKey("Customer.id"),nullable=False)
    date_of_request=db.Column(db.Date,nullable=True)
    status=db.Column(db.String,nullable=True)
    date_of_completion=db.Column(db.Date,nullable=True)
    remarks=db.Column(db.String,nullable=True)
    rating=db.Column(db.Integer,default=0)
    service=db.relationship("Service",cascade="all,delete",backref="Servicereq",lazy=True)
    
#Entity 6
class subservice(db.Model):
    __tablename__="subservice"
    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String,nullable=False)
    description=db.Column(db.String,nullable=False)
    baseprice=db.Column(db.Integer,default=0.0)
    location=db.Column(db.String,nullable=False)
    pincode=db.Column(db.String,nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('Service.id'), nullable=False)
    
                    