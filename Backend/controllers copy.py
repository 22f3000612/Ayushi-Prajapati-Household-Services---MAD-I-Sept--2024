#App routes
from flask import Flask,render_template,request,redirect,url_for,session
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
        print(usr)
        if usr:
            return redirect(url_for("admin_dashboard",name=uname))        
        usr1=Customer.query.filter_by(email=uname,password=pwd).first()
        if usr1 and usr1.status=='Blocked':
            return render_template("login.html",msg='Your account has been blocked')
        usr2=Professional.query.filter_by(email=uname,password=pwd).first()
        if usr2 and usr2.status=='Blocked':
            return render_template("login.html",msg='Your account has been Blocked')
        if usr2 and usr2.p_req=="Approved":
            return redirect(url_for("professional_dashboard",name=uname))
        if usr2 and usr2.p_req=="Declined":
            return render_template("login.html",msg='We are Sorry your request has been Declined')
        if usr2 and usr2.p_req=='Pending':
            return render_template("login.html",msg='Your request is Pending')        
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
        new_usr = Customer(email=uname1, password=pwd1, fullname=full_name1, address=address1, pincode=pinCode1, contact_number=contact_number1,status='Active')
        db.session.add(new_usr)
        db.session.commit()
        return render_template("login.html",msg="Register Successful, login now")   
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
        new_usr=Professional(email=uname2,password=pwd2,fullname=full_name2,address=address2,pincode=pincode2,contact_number=contact_number2,experience=experience2,service_name=service_name2,professional_summary=professional_summary2,p_req='Pending',status='Active')
        db.session.add(new_usr)
        db.session.commit()
        return render_template("login.html",msg="Register Successful, login now")   
    return render_template("signup_sp.html")



@app.route("/service/<name>",methods=["POST","GET"])
def service(name):
    if request.method=="POST":
        sname=request.form.get("name")
        sprice=request.form.get("baseprice")
        sdesc=request.form.get("description")
        ssubs=request.form.get("subservice")
        sloc=request.form.get("location")
        spincode=request.form.get("pincode")
        new_service=Service(name=sname,baseprice=sprice,description=sdesc,subservice=ssubs,location=sloc,pincode=spincode)
        db.session.add(new_service)
        db.session.commit()
        return redirect(url_for("admin_dashboard",name=name,msg="Service Added Successfully"))
    return render_template("addservice.html",name=name)


        
#other supported function
def get_services():
    services=Service.query.all()
    return services
def get_customer():
    customers=Customer.query.all()
    return customers
def get_professional():
    professionals=Professional.query.all()
    return professionals

@app.route("/admin/<name>")
def admin_dashboard(name):
    services=get_services()
    customers=get_customer()
    professionals=get_professional()

    return render_template("admindashboard.html",name=name,services=services,customers=customers,professionals=professionals)

@app.route("/customer/<name>")
def customer_dashboard(name):
    services=get_services()
    return render_template("Customerdashboard.html",name=name,services=services)

@app.route("/professional/<name>")
def professional_dashboard(name):
    return render_template("Professionaldashboard.html",name=name)


@app.route("/customer/<name>",methods=["POST","GET"])
def customer(name):
    if request.method=="POST":
        cname=request.form.get("fullname")
        ccntn=request.form.get("contact_number")
        cadd=request.form.get("address")
        cpin=request.form.get("pincode")
        return redirect(url_for("admin_dashboard",name=name,fullname=cname,contact_number=ccntn,address=cadd,pincode=cpin))
    return render_template("addcustomer.html",name=name)


@app.route("/profesional/<name>",methods=["POST","GET"])
def professional(name):
    if request.method=="POST":
        pname=request.form.get("fullname")
        pcntn=request.form.get("contact_number")
        psn=request.form.get("service_name")
        pexp=request.form.get("experience")
        pps=request.form.get("professional_summary")
        return redirect(url_for("admin_dashboard",name=name,fullname=pname,contact_number=pcntn,service_name=psn,experience=pexp,professional_summary=pps))
    return render_template("addprofessional.html",name=name)
 
       
@app.route("/delete_service/<id>", methods=["GET"])
def delete_service(id):
    service = Service.query.get(id)
    db.session.delete(service)
    db.session.commit()
    return redirect(url_for("admin_dashboard", name="Admin"))

@app.route("/delete_customer/<id>", methods=["GET"])
def delete_customer(id):
    customer = Customer.query.get(id)
    db.session.delete(customer)
    db.session.commit()
    return redirect(url_for("admin_dashboard", name="Admin"))

@app.route("/delete_professional/<id>", methods=["GET"])
def delete_professional(id):
    professional = Professional.query.get(id)
    db.session.delete(professional)
    db.session.commit()
    return redirect(url_for("admin_dashboard", name="Admin"))



@app.route("/edit_service/<id>", methods=["GET", "POST"])
def edit_service(id):
    service = Service.query.get(id)   
    if request.method == "POST":
        service.name = request.form.get("name")
        service.baseprice = request.form.get("baseprice")
        service.description = request.form.get("description")
        db.session.commit()
        return redirect(url_for("admin_dashboard", name="Admin"))
    return render_template("EorDservices.html", service=service)


@app.route("/approve_professional/<id>",methods=["GET","POST"])
def approve_professional(id):
    professional=Professional.query.get(id)
    if professional:
        professional.p_req="Approved"
        db.session.commit()
        return redirect(url_for("admin_dashboard",name="Admin"))
    
    
@app.route("/decline_professional/<id>",methods=["GET","POST"])
def decline_professional(id):
    professional=Professional.query.get(id)
    if professional:
        professional.p_req="Declined"
        db.session.commit()
        return redirect(url_for("admin_dashboard",name="Admin"))

@app.route("/blocked_professional/<id>",methods=["GET","POST"])
def blocked_professional(id):
    professional=Professional.query.get(id)
    if professional:
        professional.status="Blocked"
        db.session.commit()
        return redirect(url_for("admin_dashboard",name="Admin"))

@app.route("/active_professional/<id>",methods=["GET","POST"])
def active_professional(id):
    professional=Professional.query.get(id)
    if professional:
        professional.status="Active"
        db.session.commit()
        return redirect(url_for("admin_dashboard",name="Admin"))
    

@app.route("/blocked_customer/<id>",methods=["GET","POST"])
def blocked_customer(id):
    customer=Customer.query.get(id)
    if customer:
        customer.status="Blocked"
        db.session.commit()
        return redirect(url_for("admin_dashboard",name="Admin"))

    
@app.route("/active_customer/<id>",methods=["GET","POST"])
def active_customer(id):
    customer=Customer.query.get(id)
    if customer:
        customer.status="Active"
        db.session.commit()
        return redirect(url_for("admin_dashboard",name="Admin"))
    

@app.route("/search/<name>",methods=["GET","POST"])
def search(name):
    if request.method=="POST":
        search_txt=request.form.get("search_txt")
        by_professionalname=search_by_professionalname(search_txt)
        by_professionaladdress=search_by_professionaladdress(search_txt)
        by_professionalpincode=search_by_professionalpincode(search_txt)
        if by_professionalname:
            return render_template("admindashboard.html",professionals=by_professionalname)
        if by_professionaladdress:
            return render_template("admindashboard.html",professionals=by_professionaladdress)
        if by_professionalpincode:
            return render_template("admindashboard.html",professionals=by_professionalpincode)
               
    return render_template("admindashboard.html",name=name)

def search_by_professionalname(search_txt):
    professionals=Professional.query.filter(Professional.fullname.ilike("%{search_txt}%")).all
    return professionals

def search_by_professionaladdress(search_txt):
    professionals=Professional.query.filter(Professional.address.ilike("%{search_txt}%")).all
    return professionals

def search_by_professionalpincode(search_txt):
    professionals=Professional.query.filter(Professional.pincode.ilike("%{search_txt}%")).all
    return professionals


@app.route("/subservice/<id>")
def Subservice(id):
    service=Service.query.get(id)
    if service:
        subservices = subservice.query.filter_by(id=id).all()
        return render_template("subservice.html",subservices=subservices,service=service)
    return render_template("Customerdashboard.html",msg="No Services Found")


@app.route("/subservices/<int:subservice_id>",methods=["POST","GET"])
def subservices(subservice_id):
    if request.method=="POST":
        ssname=request.form.get("name")
        ssprice=request.form.get("baseprice")
        ssdesc=request.form.get("description")
        ssloc=request.form.get("location")
        sspincode=request.form.get("pincode")
        new_subservice=subservice(name=ssname,baseprice=ssprice,description=ssdesc,location=ssloc,pincode=sspincode,service_id=subservice_id)
        db.session.add(new_subservice)
        db.session.commit()
        return redirect(url_for("admin_dashboard",name="Admin", msg="Subservice Added Successfully"))
    return render_template("addsubservice.html",subservice_id=subservice_id)


@app.route("/booking/<int:subservice_id>",methods=["GET"])
def bookin(subservice_id):
    print(subservice_id)
    
    new_subservice=Servicereq(Service_id=subservice_id,baseprice=ssprice)
    db.session.add(new_subservice)
    db.session.commit()

    return redirect(url_for("admin_dashboard",name="Admin", msg="Subservice Added Successfully"))






