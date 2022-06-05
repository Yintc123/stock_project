from flask import *
from dotenv import load_dotenv, dotenv_values
from .email_module import *
import random


env='.env' # 執行環境
load_dotenv(override=True)

app_email=Blueprint("api_email", __name__)

url_email="/email"
@app_email.route(url_email, methods=["POST"])
def verify_email():
    verified_email=request.form.get("email")
    number=produce_verif_number()
    gmail=gmail_module(verified_email, "驗證碼")
    msg="您的驗證碼為"+number
    gmail.send_message(msg)
    session["email_verification"]=number
    return number

def produce_verif_number():
    number=str(random.randint(0,9999)/10000)
    number=number[2:]
    if len(number)<4:
        for index in range(4-len(number)):
            number+="0"     
    return number

        
