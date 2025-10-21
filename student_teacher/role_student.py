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
      
   