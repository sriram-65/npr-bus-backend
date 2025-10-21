from flask import Flask , Blueprint , redirect , request , jsonify , session
from firebase_admin import auth , credentials
from .handlers import Show_Bad_Error , Show_Server_Error , Show_Success_Msg
import firebase_admin
import datetime
from db.db import STUDENTS
from utils.helper import JSON_Parser , Check_Role

Auth = Blueprint("Auth" , __name__)


cred = credentials.Certificate('fir-c24bc-firebase-adminsdk-olzh6-5d58acd2ef.json')
firebase_admin.initialize_app(cred)


@Auth.route("/google" , methods=['POST'])
def Google_Login():
    try:
        token = request.json.get("token")
        if not token:
            return jsonify(Show_Bad_Error("Pls Provide The Id Token")) , 400
        
        student_data = auth.verify_id_token(token)
        if student_data:

            Student_name = student_data.get("name")
            Student_Email = student_data.get("email")
             

            if not Student_name or not Student_Email:
                return jsonify(Show_Bad_Error("Unable to Fetch Student deatils")) , 400

            Student_pic = student_data.get("picture")
            Student_Uid = student_data.get("uid")
            Student_Phone_no = student_data.get("phone_number" , False)
            Student_email_Verfication = student_data.get("email_verified")
            
            Student = STUDENTS.find_one({"_Email":Student_Email})
            if not Student:
                res = Create_Student(Student_name , Student_Email , Student_Uid , Student_pic , Student_Phone_no , Student_email_Verfication , new=True)
                
                if res.get("Success")==True:
                    return jsonify(Show_Success_Msg(res.get('msg') , new=True , role=res.get("role"))) , 200
                else:
                    return jsonify(Show_Bad_Error(res.get("msg"))) , 400
            else:
                 res = Create_Student(email=Student['_Email']  , new=False)
                 if res.get("Success")==True:
                     return jsonify(Show_Success_Msg(res.get('msg') , new=False , role=res.get("role"))) , 200
                 else:
                    return jsonify(Show_Bad_Error(res.get("msg"))) , 400
                                  
        else:
            return jsonify(Show_Bad_Error("Token is Invalied"))
        
    except  Exception as e:
        print(e)
        return jsonify(Show_Server_Error()) , 500



def Create_Student(name='op' , email=None , uid='op' , pic='op' , phone='op' , email_verfied='op' , new=True):
    try:
        if new==True:
            set_role = Check_Role(email)
             
            if set_role.get("yes")==False:
                data = {
                    "_Name":name,
                    "_Email":email,
                    "Uid":uid,

                    "From_Google":{
                        "Pic":pic,
                        "Phone_no":phone,
                        "Email_Verfication":email_verfied
                    },
                    
                    "Offical_Phone_no":None,
                    "Department":None,
                    "Year":None,
                    "Bus_No":None,
                    "Gender":None,
                    "Updated":False,
                    "Role":"Student",
                    "User_Created_at":datetime.datetime.utcnow()
                }
                STUDENTS.insert_one(data)
                session['email'] = data['_Email']
                session['role'] = data['Role']

            elif set_role.get("yes")==True:
                data = {
                    "_Name":name,
                    "_Email":email,
                    "Uid":uid,

                    "From_Google":{
                        "Pic":pic,
                        "Phone_no":phone,
                        "Email_Verfication":email_verfied
                    },
                    
                    "Offical_Phone_no":set_role['admin_data']['phone'],
                    "Bus_No":set_role['admin_data']['busno'],
                    "Gender":set_role['admin_data']['gender'],
                    "Role":"Admin",
                    "User_Created_at":datetime.datetime.utcnow()
                }
                STUDENTS.insert_one(data)
                session['email'] = data['_Email']
                session['role'] = data['Role']
            else:
                return jsonify(Show_Bad_Error("Unexpected Error Occured")) , 400
            
            return {"msg":"User Created and inserted Sucessfully"  , 'new':True , 'role':session['role'], "Success":True}
        else:
            session['email'] = email
            Get_role = STUDENTS.find_one({"_Email":email})
            session['role'] = Get_role['Role']
            return {"msg":"User Created and intialzed Sucessfully"  , 'new':False , 'role':Get_role['Role'],  "Success":True}
    except:
        return jsonify(Show_Bad_Error("Unexpted Error !"))  , 400


            
@Auth.route('/me' , methods=['GET'])
def Me():
    try:
        email = session.get("email")
        if email:
            student = STUDENTS.find_one({"_Email":email})
            if student:
                student['_id'] = str(student['_id'])
                return jsonify({"Success":True , "data":student})
            else:
                return jsonify({"Success":False , 'Error':"Noo Student Found"})
        else:
            return jsonify({"Success":False , 'Error':"Session was Not Found"})
    except:
        return jsonify(Show_Server_Error()) , 500


@Auth.route('/update/<uid>' , methods=['POST'])
def Update_Student(uid):
    try:
        student = STUDENTS.find_one({"Uid":uid})
        if not student:
            return jsonify(Show_Bad_Error("Student Not Found")) , 400
        
        phone_no = request.json.get("pn")
        dep = request.json.get("dep")
        year = request.json.get("year")
        busno = request.json.get("busno")
        gender = request.json.get("gender")
        

        if not phone_no or not dep or not year or not busno or not gender:
            return jsonify(Show_Bad_Error("Pls Provide All Feilds")) , 400
        
        STUDENTS.find_one_and_update({"Uid":uid} , {"$set":{
            "Offical_Phone_no":int(phone_no),
            "Department":dep,
            "Year":year,
            "Bus_No":int(busno),
            "Gender":gender,
            "Updated":True
        }})

        return jsonify({"Success":True , "msg":"Student Data Has Been Updated Successfully"}) , 200
    except Exception as e:
        return jsonify(Show_Server_Error())



        