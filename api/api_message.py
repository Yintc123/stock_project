from flask import *
from data.message_db import message_db
from data.member_db import member_db
from dotenv import load_dotenv, dotenv_values

error={
    "error":True,
    "message":None
}

env='.env' # 執行環境
load_dotenv(override=True)

app_message=Blueprint("api_message", __name__)

url_message="/message/<stock_id>"
@app_message.route(url_message, methods=["GET"])
def get_message(stock_id):
    data={
        "data":None
    }
    msg_db=message_db()
    mb_db=member_db()
    data["data"]=msg_db.get_message(stock_id)
    # data["data"].reverse() # 反轉list，從新到舊排列

    for msg in data["data"]:
        member_data=mb_db.get_member(None, msg["user_id"])
        msg["username"]=member_data["username"]
        if member_data["photo"]:
            member_data["photo"]=dotenv_values(env)["url_cdn"]+member_data["photo"]
        msg["photo"]=member_data["photo"]

    return data

@app_message.route(url_message, methods=["POST"])
def add_message(stock_id):
    user_id=request.form.get("user_id")
    message=request.form.get("message")
    msg_db=message_db()
    resp=msg_db.add_message(user_id, stock_id, message)

    return resp

@app_message.route(url_message, methods=["DELETE"])
def delete_message(stock_id):
    msg_db=message_db()
    resp=msg_db.delete_message(stock_id)

    return resp