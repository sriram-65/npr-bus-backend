import random as r
import datetime

def Generate_OTP():
   otp_number = r.randint(21473 , 46599)
   if otp_number:
      return otp_number
   else:
      return False
