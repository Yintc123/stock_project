import json
from flask import *
from dotenv import load_dotenv, dotenv_values
from pywebpush import webpush, WebPushException
from data.member_db import member_db

env='.env'
load_dotenv(override=True)

app_webpush=Blueprint("api_webpush", __name__)

@app_webpush.route('/subscription', methods=["POST"])
def subscribe():
    user_id=request.form.get("user_id")
    subscription=request.form.get("subscription")
    mb_db=member_db()
    mb_db.add_push_token(user_id, subscription)
    return {"ok":True}

@app_webpush.route('/push', methods=["POST"]) # service server會綁定subscription_token
def push():
    user_id=request.form.get("user_id")
    mb_db=member_db()
    member=mb_db.get_member(None, user_id) # 測試用
    title="到價通知"
    body="測試通知"
    payload=json.dumps({"title":title,"body":body})

    webpush(
        subscription_info=json.loads(member["push_token"]), # 將json(string) 轉成 dict
        data=payload,
        vapid_private_key=dotenv_values(env)["VAPID_private_key"],
        vapid_claims={
            "sub": "mailto:{}".format(dotenv_values(env)["gmail"])
        }
    )
    return {"ok":True}
