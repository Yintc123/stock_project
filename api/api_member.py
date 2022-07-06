import datetime
from flask import *
from data.member_db import member_db
from data.stock_db import stock_info_db
from .api_aws import Aws_s3_api
from dotenv import load_dotenv, dotenv_values
import jwt

env='.env' # 執行環境
load_dotenv(override=True)

member_key=dotenv_values(env)["member_key"] # jwt_key

error={
    "error":True,
    "message":None
}

app_member=Blueprint("api_member", __name__)

url_member="/member"
@app_member.route(url_member, methods=["GET"])
def get_member():
    token_member=request.cookies.get("token_member")
    if token_member:
        member=jwt.decode(token_member, member_key, algorithms="HS256")
        member.pop("exp")
        return member
    return {"data":None}

@app_member.route(url_member, methods=["DELETE"])
def signOut_member():
    resp=make_response({"ok":True})
    resp.set_cookie(key="token_member", expires=0) # 將cookie的到期時間設定為0，清除cookie
    return resp

@app_member.route(url_member, methods=["POST"])
def create_member():
    username=request.form.get("username")
    email=request.form.get("email")
    password=request.form.get("password")
    if not username:
        error["message"]="請輸入使用者名稱"
        return error
    if not email:
        error["message"]="請輸入email"
        return error
    if "@" not in email:
        error["message"]="註冊失敗，Email格式有誤"
        return error
    if not password:
        error["message"]="請輸入密碼"
        return error
    mb_db=member_db()
    member_info=mb_db.get_member(email, None)
    if member_info:
        error["message"]="此email已註冊"
        return error
    result=mb_db.create_member(username, email, password)
    if result:
        return {"ok":True, "message":"註冊成功!"}
    error["message"]=result["message"]
    return error

@app_member.route(url_member, methods=["PATCH"])
def signIn_member():
    member={"data":{
        "id":None,
        "username":None,
        "email":None,
        "photo":None,
        "email_status":None,
        "favorite":[]
    }}
    email=request.form.get("email")
    password=request.form.get("password")
    if not email:
        error["message"]="請輸入email"
        return error
    if not password:
        error["message"]="請輸入密碼"
        return error
    mb_db=member_db()
    member_info=mb_db.get_member(email, None)
    if not member_info:
        error["message"]="此email未註冊"
        return error
    if member_info["password"] != password:
        error["message"]="密碼輸入錯誤"
        return error

    print(member_info)
    resp=make_response({"ok":True, "message":"登入成功!"})
    for info in member["data"]:
        if info=="photo" and member_info[info]:
            member["data"][info]=dotenv_values(env)["url_cdn"]+member_info[info]
            continue
        if info=="favorite":
            favorite=mb_db.get_favorite_stock(member_info["id"])
            add_stock_name(favorite)
            member["data"][info]=favorite
            continue
        member["data"][info]=member_info[info]
    
    payload=member
    payload["exp"]=datetime.datetime.utcnow()+datetime.timedelta(days=30) #設定token於30天到期
    token_member=jwt.encode(payload, member_key, algorithm="HS256") #token加密
    resp.set_cookie(
                key="token_member",
                value=token_member,
                expires=datetime.datetime.utcnow()+datetime.timedelta(days=30) #設定cookie於30天到期
            )

    return resp

url_member_id="/member/<member_id>"
@app_member.route(url_member_id, methods=["PATCH"])
def renew_member(member_id):
    token_member=request.cookies.get("token_member") # 確定發送request的人為該帳號的使用者
    if not token_member:
        error["message"]="請登入後，再修改使用者資訊"
        return error
    payload_member=jwt.decode(token_member, member_key, algorithms="HS256")
    if payload_member["data"]["id"] != int(member_id):
        error["message"]="勿修改他人資訊"
        return error

    img_filename=None
    username=request.form.get("username")
    email=request.form.get("email")
    email_verification=request.form.get("email_verification")
    password=request.form.get("password")
    photo=request.files.get("photo") # js回傳null，python讀取為字串null非None

    member_info={
        "username":username,
        "email":email,
        "password":password,
        "photo":img_filename,
        "email_status":payload_member["data"]["email_status"]
    }

    if not photo:
        if not username:
            error["message"]="請輸入使用者名稱"
            return error
        if not email:
            error["message"]="請輸入email"
            return error
        if "@" not in email:
            error["message"]="Email格式有誤"
            return error
        if payload_member["data"]["email"]!=email:
            if email_verification!=session["email_verification"]:
                error["message"]="Email驗證碼有誤"
                return error
            member_info["email_status"]=1
        if email_verification:
            if email_verification!=session["email_verification"]:
                error["message"]="Email驗證碼有誤"
                return error
            member_info["email_status"]=1
        if not password:
            error["message"]="請輸入密碼"
            return error
    else: # 如果上傳照片
        file=photo.read()
        img_format=photo.filename.split(".")[1]
        s3=Aws_s3_api()
        timeString = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S") # 由於時間不會重複，圖片以時間命名，以免使用cdn系統抓到同名但內容的圖片
        img_filename=s3.upload_data(file, img_format, timeString)
        member_info["photo"]=dotenv_values(env)["url_cdn"]+img_filename # 更新圖片路徑

    mb_db=member_db()
    result=mb_db.renew_member(member_id, username, email, password, img_filename, member_info["email_status"])

    for info in (payload_member["data"] and member_info): # 更新jwt token
        if member_info[info]==None or member_info[info]=="null" or member_info[info]=="":
            continue
        payload_member["data"][info]=member_info[info]
    token_member=jwt.encode(payload_member, member_key, algorithm="HS256") #token加密
    resp=make_response(result)
    resp.set_cookie(
            key="token_member",
            value=token_member,
    )

    return resp

@app_member.route(url_member_id, methods=["POST"])
def get_all_member_info(member_id):
    member_info={"data":{
        "email":None,
        "username":None,
        "password":None,
        "photo":None
    }}

    token_member=request.cookies.get("token_member") # 確定發送request的人為該帳號的使用者
    if not token_member:
        error["message"]="請登入後，再查詢使用者資訊"
        return error
    member=jwt.decode(token_member, member_key, algorithms="HS256")
    # member.pop("exp")
    if member["data"]["id"] != int(member_id):
        error["message"]="勿查詢他人資訊"
        return error
    member_info["email"]=member["data"]["email"]
    
    mb_db=member_db()
    member_info["data"]=mb_db.get_member(member_info["email"], None)

    return member_info

url_member_id_stock="/member/<member_id>/<stock_id>"
@app_member.route(url_member_id_stock, methods=["GET"])
def get_favorite_stock(member_id, stock_id):
    data={"data":None}
    mb_db=member_db()
    data["data"]=mb_db.get_favorite_stock(member_id)
    return data

@app_member.route(url_member_id_stock, methods=["POST"])
def add_favorite_stock(member_id, stock_id):
    token_member=request.cookies.get("token_member") # 確定發送request的人為該帳號的使用者
    if not token_member:
        error["message"]="請登入後，再添加股票至我的最愛"
        return error
    payload_member=jwt.decode(token_member, member_key, algorithms="HS256")
    if payload_member["data"]["id"] != int(member_id):
        error["message"]="勿修改他人資訊"
        return error

    mb_db=member_db()
    response=mb_db.add_favorite_stock(member_id, stock_id)
    favorite=mb_db.get_favorite_stock(member_id)
    add_stock_name(favorite)
    payload_member["data"]["favorite"]=favorite

    token_member=jwt.encode(payload_member, member_key, algorithm="HS256") #token加密
    resp=make_response(response) # 更新token
    resp.set_cookie(
            key="token_member",
            value=token_member,
    )

    return resp

@app_member.route(url_member_id_stock, methods=["DELETE"])
def delete_favorite_stock(member_id, stock_id):
    token_member=request.cookies.get("token_member") # 確定發送request的人為該帳號的使用者
    if not token_member:
        error["message"]="請登入後，再刪除關注股票"
        return error
    payload_member=jwt.decode(token_member, member_key, algorithms="HS256")
    if payload_member["data"]["id"] != int(member_id):
        error["message"]="勿修改他人資訊"
        return error

    mb_db=member_db()
    response=mb_db.delete_favorite_stock(member_id, stock_id)
    
    favorite=mb_db.get_favorite_stock(member_id)
    add_stock_name(favorite)
    payload_member["data"]["favorite"]=favorite
    

    token_member=jwt.encode(payload_member, member_key, algorithm="HS256") #token加密
    resp=make_response(response) # 更新token
    resp.set_cookie(
            key="token_member",
            value=token_member,
    )

    return resp

@app_member.route(url_member_id_stock, methods=["PATCH"])
def add_price_notification(member_id, stock_id):
    token_member=request.cookies.get("token_member") # 確定發送request的人為該帳號的使用者
    if not token_member:
        error["message"]="請登入後，再添加股價至我的最愛"
        return error
    payload_member=jwt.decode(token_member, member_key, algorithms="HS256")
    if payload_member["data"]["id"] != int(member_id):
        error["message"]="勿修改他人資訊"
        return error

    price=request.form.get("price")
    # if not price:
    #     error["message"]="請輸入股價"
    #     return error

    mb_db=member_db()
    response=mb_db.add_favorite_stock_price(member_id, stock_id, price)

    favorite=mb_db.get_favorite_stock(member_id)
    add_stock_name(favorite)
    payload_member["data"]["favorite"]=favorite

    token_member=jwt.encode(payload_member, member_key, algorithm="HS256") #token加密
    resp=make_response(response) # 更新token
    resp.set_cookie(
            key="token_member",
            value=token_member,
    )

    return resp

def add_stock_name(lst):
    stk_db=stock_info_db()
    i=1
    for favorite in lst:
        stock_name=stk_db.get_stock_name(favorite["stock_id"])
        favorite["stock_name"]=stock_name["stock_name"]
        favorite["index"]=i
        i+=1
    return lst
        