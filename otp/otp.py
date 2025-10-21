from flask import Flask , Blueprint , request , jsonify
from db.db import REGISTERS_OTP_BUSES  , STUDENTS  , STUDENTS_OTP
from auth.handlers import Show_Bad_Error , Show_Server_Error
from utils.generate_otp import Generate_OTP
import datetime

Otp = Blueprint("Otp" , __name__)

@Otp.route("/generate/student/placeholder" , methods=['POST'])
def Gen_otp_Place():
    try:

        uid = request.json.get("uid")
        date = request.json.get("date")
        today = datetime.date.today().strftime("%d-%m-%Y")
        
        if not uid:
            return jsonify(Show_Bad_Error("UID is invalid")) , 400
        
        if date!=today:
            return jsonify(Show_Bad_Error("The Date Must Be Today")) , 400
        
        Student = STUDENTS.find_one({"Uid":uid})
        
        if not Student:
            return jsonify(Show_Bad_Error(f"Student Not Found at this UID , {uid}")) , 400
        
        
        find_placeholder =  STUDENTS_OTP.find_one({"uid":uid , "date":date})
        if find_placeholder:
            return jsonify(Show_Bad_Error(f"Already Placeholder Created For this date , {date}")) , 400
        
        data = {
            "name":Student.get("_Name"),
            "email":Student.get("_Email"),
            "Attendanced_By":None,
            "uid":uid,
            "otp_verfied":False,
            "date":date,
            "busno":Student['Bus_No'],
            "Started":False,
            "created_at":datetime.datetime.utcnow()
        }
       
        STUDENTS_OTP.insert_one(data)
        data['_id'] = str(data['_id'])
        return jsonify({"Success":True , "msg":f"OTP Placeholder Created for Today , {date}" , "data":data})
    except:
        return jsonify(Show_Server_Error())


@Otp.route("/generate/otp/<busno>" , methods=['POST'])
def Generate_Otp(busno):
    try:
      Admin_Uid = request.json.get("admin_uid")
      admin = STUDENTS.find_one({"Uid":Admin_Uid})
      if not admin:
          return jsonify(Show_Bad_Error("Teacher Not Found")) , 400
      
      otp_number =  Generate_OTP()
      if otp_number:
          now = datetime.datetime.now()
          ex_time = now + datetime.timedelta(minutes=1)
          
          buses = REGISTERS_OTP_BUSES.find_one({"busno":int(busno)})
          if not buses:
                
            data = {
                "busno":int(busno),
                "Admin_uid":Admin_Uid,
                "Admin_Name":admin['_Name'],
                "otp_ex":ex_time,
                "otp_num":int(otp_number)
            }
            REGISTERS_OTP_BUSES.insert_one(data)
            return jsonify({"Success":True , "msg":"OTP instance was Created only Valid for 1 miniute" , "OTP":otp_number}), 200
          else:
            REGISTERS_OTP_BUSES.find_one_and_update({"busno":int(busno)} , {"$set":{
                "otp_ex":ex_time,
                "otp_num":otp_number
            }})
            return jsonify({"Success":True , "msg":f"OTP  Created only Valid for 1 miniute" , "OTP":otp_number}), 200
      else:
          return jsonify(Show_Bad_Error("Something Went Wrong Creating the OTP")) , 400
    except:
        return jsonify(Show_Server_Error())
    

@Otp.route("/verfiy/<busno>/" , methods=['POST'])
def Verify_Otp(busno):
    try:
        
        student_uid = request.json.get("student_uid")
        user_otp = request.json.get("user_otp")
        date = request.json.get("date")

        if not student_uid:
           return jsonify(Show_Bad_Error("Pls Provide the Student UID")) , 400
        
        Student = STUDENTS_OTP.find_one({"date":date})
        if not Student:
           return jsonify(Show_Bad_Error("Student Not Found")) , 400
    
        
        buses = REGISTERS_OTP_BUSES.find_one({"busno":int(busno)})
        if not buses:
            return jsonify(Show_Bad_Error("Bus not Found to Verify the OTP")) , 400
        
        now = datetime.datetime.now()
        if now>=buses.get("otp_ex"):
            return jsonify(Show_Bad_Error("OTP has Been Expired")), 400
        
        if buses.get("otp_num") == int(user_otp):
            STUDENTS_OTP.find_one_and_update({"date":date , "uid":student_uid} , {"$set":{
                "otp_verfied":True,
                "Attendanced_By":buses['Admin_Name']
            }})
            return jsonify({"Success":True , "msg":"OTP has Been Verfied Successfully , now Marked has PRESENT !"}) , 200
        else:
            return jsonify(Show_Bad_Error("Invalid OTP"))
    except:
        return jsonify(Show_Server_Error())





