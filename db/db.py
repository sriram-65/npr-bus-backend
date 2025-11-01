from pymongo import MongoClient

cleint = MongoClient("mongodb+srv://sriramng24_db_user:1324sriram@cluster0.efzrgtt.mongodb.net/")

db = cleint['NPR_BUS_PORTAL']
STUDENTS = db['STUDENTS']
STUDENTS_OTP = db['STUDENTS_OTP']
REGISTERS_OTP_BUSES = db['REGISTERS_OTP_BUSES']
ADMIN_EMAILS = db['ADMIN_EMAILS']
ADMIN_PLACEHOLDERS = db['ADMIN_PLACEHOLDERS']


