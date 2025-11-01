from flask import Flask , Blueprint , jsonify , request , session
from db.db import STUDENTS , STUDENTS_OTP , REGISTERS_OTP_BUSES
from utils.helper import JSON_Parser
import datetime
from auth.handlers import Show_Server_Error , Show_Bad_Error

Role_Student = Blueprint("Role_Student" , __name__)

@Role_Student.route("/")
def Get_all_Deatils():
    try:
      email = session.get("email")
      
      uid  = STUDENTS.find_one({"_Email":email})
      
      if not uid:
         return jsonify(Show_Bad_Error(f"Uid Not Found For This Email Id ")) , 400
      
      today_date = datetime.datetime.now().strftime("%d-%m-%Y")
      if email:
         placeholder = STUDENTS_OTP.find_one({"uid":uid['Uid'] , "date":today_date})
         
         if not placeholder:
            return jsonify({"Success":False , "msg":f"Placeholder Not Found for this date , {today_date}"  , 'preError':'nf'}) , 404
         
         placeholder['_id'] = str(placeholder['_id'])

         return jsonify({"Success":True , "data":placeholder}) , 200
      else:
         return jsonify(Show_Bad_Error("Session Was Not Found")) , 400
    except:
       return jsonify(Show_Server_Error())
      
@Role_Student.route("/logout")
def Logout():
   try:
      email = session.get("email")
      if not email:
         return jsonify(Show_Bad_Error("Session was Not Found")) , 400
      
      session.clear()
      return jsonify({"Success":True}) , 200
   except:
      return jsonify(Show_Server_Error()) , 500
   
@Role_Student.route("/profile")
def Profile_Student():
   try:
      email = session.get("email")
      if not email:
         return jsonify(Show_Bad_Error("Session was Not Found")) , 400
      
      student = STUDENTS.find_one({"_Email":email})
      if not student:
         return jsonify(Show_Bad_Error("Student Not Found")) , 400
      
      student['_id'] = str(student['_id'])
      return jsonify({"Success":True , 'Student':student}) , 200
   except:
      
      return jsonify(Show_Server_Error()), 500



@Role_Student.route("/history")
def Show_Histroy():
   try:
      email = session.get("email")
      if not email:
         return jsonify(Show_Bad_Error("Session was Not Found")) , 400
      
      Student_Deatils = STUDENTS.find_one({"_Email":email})
     
      if not Student_Deatils:
         return jsonify(Show_Bad_Error("Unable to Find the Student")) , 400
      
      
      Student_histroy = STUDENTS_OTP.find({"email":email , "busno":Student_Deatils['Bus_No']})
      
      if Student_histroy:
         data = JSON_Parser(Student_histroy)
        
         if data:
            return jsonify({"Success":True , "data":data}) , 200
         else:
            return jsonify(Show_Bad_Error("Unexpected Error")) , 400
      else:
         return jsonify(Show_Bad_Error("Student History Not Found")) , 400
   except Exception as e:
      print(e)
      return jsonify(Show_Server_Error()) , 500






