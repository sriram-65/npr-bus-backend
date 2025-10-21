from flask import Flask , Blueprint , request , jsonify , render_template
from db.db import REGISTERS_OTP_BUSES , STUDENTS , STUDENTS_OTP , ADMIN_EMAILS , ADMIN_PLACEHOLDERS
from auth.handlers import Show_Bad_Error , Show_Server_Error
from utils.helper import JSON_Parser

Role_Admin = Blueprint("Role_Admin" , __name__)


@Role_Admin.route('/create' , methods=['POST'])
def Create_Admin():
    try:
        Admin_email = request.json.get("Admin_email")
        phone_no = request.json.get("Phone_no")
        busno = request.json.get("busno")
        gender = request.json.get("gender")

        if not Admin_email:
            return jsonify(Show_Bad_Error("Pls Provide Email")) , 400
        
        ae = ADMIN_EMAILS.find_one({"admin_email":Admin_email})
        if ae:
            return jsonify(Show_Bad_Error("Email has Already Registerd As Admin")) , 400
        data = {
            "phone":int(phone_no),
            "busno":int(busno),
            "gender":gender,
            "admin_email":Admin_email
        }
        ADMIN_EMAILS.insert_one(data)
        data['_id'] = str(data['_id'])
        return jsonify({"Success":True , "msg":"Admin Created" , 'data':data}) , 200
    except:
        return jsonify(Show_Server_Error())



@Role_Admin.route("/session/create/<admin_uid>/<date>")
def Create_Session_Attedance(admin_uid , date):
    try:
        Admin = STUDENTS.find_one({"Uid":admin_uid})

        PlceHolder = ADMIN_PLACEHOLDERS.find_one({"date":date})

        if not Admin:
            return render_template("Err.html" , e='Admin was not Found')
        
        if PlceHolder:
            return render_template("att_session.html" , admin=Admin)
        
        STUDENTS_OTP.update_many({"date":date} , {"$set":{
            "Started":True
        }})

        data = {
            "Admin_uid":admin_uid,
            "date":date,
            "Admin_Name":Admin['_Name'],
            "Admin_Email":Admin['_Email']
        }
        ADMIN_PLACEHOLDERS.insert_one(data)

        return render_template("att_session.html" , admin=Admin)
    except:
            return render_template("Err.html" , e='Server Error')


@Role_Admin.route("/check-session/<date>")
def Check_Session(date):
    try:
        ap = ADMIN_PLACEHOLDERS.find_one({"date":date})
        if not ap:
            return jsonify(Show_Bad_Error("Not Found")) , 404
        ap['_id'] = str(ap['_id'])
        return jsonify({"Success":True , "data":ap}) , 200
    except:
        return jsonify(Show_Server_Error())

# @Role_Admin.route('/sort/<sortby>/<busno>')
# def sortBy(sortby , busno):
#     try:
#        split_section = sortby.split(":")
#        if split_section:
           
#     except:
#         return jsonify("error")


 
@Role_Admin.route("/get-students/<busno>/<date>")
def Get_Stuents(busno , date):
    try:
        student_placeholders = STUDENTS_OTP.find({"busno":int(busno) , "date":date})
        data = JSON_Parser(student_placeholders)
        if data:
            return jsonify({"Success":True , "data":data})
        else:
            return jsonify({"Success":False})
    except:
        return jsonify(Show_Server_Error())


        




