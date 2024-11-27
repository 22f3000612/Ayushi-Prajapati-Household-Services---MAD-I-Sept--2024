#App routes
from flask import Flask,render_template,request,redirect,url_for
from flask import current_app as app
from .models import *
import os

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login",methods=["GET","POST"])
def signin():
    if request.method=="POST":
        uname=request.form.get("User_name")
        pwd=request.form.get("Password")
        usr=Admin.query.filter_by(email=uname,password=pwd).first()
        if usr:
            return render_template("admindashboard.html")
        
        usr1=Customer.query.filter_by(email=uname,password=pwd).first()
        if usr1:
                return render_template("Customerdashboard.html")
        
        usr2=Professional.query.filter_by(email=uname,password=pwd).first()
        if usr2:
            return render_template("Professionaldashboard.html")
        
        else:
            return render_template("login.html",msg='Invalid Credentials')
        
    return render_template("login.html",msg='')        
        
    

@app.route("/register as customer",methods=["GET","POST"])
def signup_C():
    if request.method=="POST":
        uname1=request.form.get("User_name")
        pwd1=request.form.get("Password")
        full_name1=request.form.get("fullname")
        address1=request.form.get("address")
        pinCode1=request.form.get("pincode")
        contact_number1=request.form.get("contact_number")
        new_usr = Customer(email=uname1, password=pwd1, fullname=full_name1,
                           address=address1, pincode=pinCode1, contact_number=contact_number1)
        db.session.add(new_usr)
        db.session.commit()
        return render_template("login.html")
   
    return render_template("signup_c.html")

@app.route("/register as professional",methods=["GET","POST"])
def signup_sp():
    if request.method=="POST":
        uname2=request.form.get("User_name")
        pwd2=request.form.get("password")
        full_name2=request.form.get("fullname")
        address2=request.form.get("address")
        pincode2=request.form.get("pincode")
        contact_number2=request.form.get("contact_number")
        experience2=request.form.get("experience")
        service_name2=request.form.get("service_name")
        professional_summary2 = request.form.get("professional_summary")        
        new_usr=Professional(email=uname2,password=pwd2,fullname=full_name2,address=address2,pincode=pincode2,contact_number=contact_number2,experience=experience2,service_name=service_name2,professional_summary=professional_summary2)
        db.session.add(new_usr)
        db.session.commit()
        return render_template("login.html")
   
    return render_template("signup_sp.html")
