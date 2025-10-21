from flask import Flask 
from auth.login import Auth
from otp.otp import Otp
from student_teacher.role_student import Role_Student
from student_teacher.role_admin import Role_Admin
from flask_cors import CORS

app = Flask(__name__)
CORS(app , supports_credentials=True)

app.secret_key = '@MAHAKALI@THUNAI'

app.register_blueprint(Auth , url_prefix='/api/auth')
app.register_blueprint(Otp , url_prefix='/api/otp')
app.register_blueprint(Role_Student , url_prefix='/api')
app.register_blueprint(Role_Admin , url_prefix='/api/admin')

if __name__ == "__main__":
    app.run(debug=True)