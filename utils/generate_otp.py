import random as r
import datetime

def Generate_OTP():
   otp_number = r.randint(2143 , 9599)
   if otp_number:
      return otp_number
   else:
      return False