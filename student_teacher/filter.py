from flask import Flask , Blueprint , request , jsonify
from db.db import STUDENTS , STUDENTS_OTP
from auth.handlers import Show_Bad_Error , Show_Server_Error
from utils.helper import Filter_Options  , JSON_Parser

Filter = Blueprint("Filter" , __name__)

@Filter.route("/<int:busno>/<date>/")
def Filters(busno , date):
    try:
        dep = request.args.get("dep")
        year = request.args.get("year")
        gender = request.args.get("gender")
        
        if not dep or not year or not gender:
            return jsonify(Show_Bad_Error("Unexpected Error !")) , 400
        
        query = Filter_Options(dep , year , gender , busno , date)
    
        if query or query=={}:
            students_otps = STUDENTS_OTP.find(query)
        
            data = JSON_Parser(students_otps)
            if data == []:
                return Show_Bad_Error("Student Not Found") , 404
            
            return jsonify({"Success":True , 'data':data}) ,   200
        
        return jsonify(Show_Bad_Error("Query has Been Invalied")) , 400
    
    except:
        return jsonify(Show_Server_Error()) , 500



@Filter.route('/set/absent' , methods=['POST'])
def Set_Absent():
    try:
        Student_uid = request.json.get("suid")
        date = request.json.get("date")
        busno = request.json.get("busno")

        if not Student_uid or not date or not busno:
            return jsonify(Show_Bad_Error("Unexpected Error")) , 400
        
        Check_Student = STUDENTS_OTP.find_one({"uid":Student_uid , "busno":int(busno) , "date":date})
        if not Check_Student:
            return jsonify(Show_Bad_Error("Student Not Found")) , 400
        
        STUDENTS_OTP.find_one_and_update({"uid":Student_uid , "busno":int(busno) , "date":date} , {"$set":{
            "otp_verfied":False,
            "Attendanced_By":"Rejected"
        }})
        return jsonify({"Success":True , "msg":'Student Has Been Marked as Absent'}) , 200
    except:
        return jsonify(Show_Server_Error()) , 500


