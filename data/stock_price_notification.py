import json
import time
from data.member_db import member_db
from api.email_module import *
from flask_apscheduler import APScheduler
from pywebpush import webpush, WebPushException
from concurrent.futures import ThreadPoolExecutor
import twstock

twstock.realtime.mock = False

def send_notification():
    send_mail("yiqazwsx123@gmail.com", "到通知開始")
    while(True):
        mb_db=member_db()
        favorite=mb_db.get_all_favorite_stock()
        target_stk_list=[]
        notification_list={}
        for stock in favorite:
            if not stock["price"]:
                # print("未設定到價通知")
                continue
            if stock["stock_id"] in target_stk_list: # 股票不重複
                user_dict={"user_id":stock["user_id"], "price":stock["price"]}
                notification_list[stock["stock_id"]].append(user_dict)
                continue
            target_stk_list.append(stock["stock_id"])
            user_dict={"user_id":stock["user_id"], "price":stock["price"]}
            notification_list[stock["stock_id"]]=[]
            notification_list[stock["stock_id"]].append(user_dict)

        if target_stk_list: # 有設定到價通知才執行以下程式碼
            realtime_data=get_realtime_data(target_stk_list)
            realtime_data.pop('success', None) # 去除不必要的資訊
            clock=None
            for stock_id in realtime_data:
                clock=realtime_data[stock_id]["timestamp"]
                check_realtime_price(stock_id, realtime_data[stock_id]["realtime"]["low"], realtime_data[stock_id]["realtime"]["high"], notification_list[stock_id], mb_db)   
            clock=time.strftime("%H", time.localtime(clock))
            if clock=="14": # 14點時關閉apscheduler
                # print(clock)
                break
            time.sleep(120) # 每2分鐘確認一次即時股票資訊

def get_realtime_data(stk_list):
    return twstock.realtime.get(stk_list)

def check_realtime_price(stock_id, stock_price_low, stock_price_high, notification_list, db):   
    for user in notification_list:
        if float(stock_price_low) <= user["price"] and user["price"] <= float(stock_price_high): # 觸發到價通知
            # print("到價通知")
            member=db.get_member(None, user["user_id"])
            msg=stock_id+"已達到您設定的價格"+str(user["price"])
            with ThreadPoolExecutor(max_workers=2) as executor: # 平行任務處理 ( 非同步 ) 的功能，能夠同時處理多個任務
                executor.submit(send_web, member["push_token"], msg) # 網站推播
                if member["email_status"]==1: # 如果email認證通過
                    executor.submit(send_mail, member["email"], msg) # mail通知
            db.add_favorite_stock_price(user["user_id"], stock_id, None) # 通知結束，將通知價格設定為0，避免通知太多
    return 0

def send_web(push_token, msg): # 網站推播
    title="到價通知"
    payload=json.dumps({"title":title,"body":msg})
    webpush(
        subscription_info=json.loads(push_token), # 將json(string) 轉成 dict
        data=payload,
        vapid_private_key=dotenv_values(env)["VAPID_private_key"],
        vapid_claims={
            "sub": "mailto:{}".format(dotenv_values(env)["gmail"])
        }
    )
    return 0

def send_mail(email, msg): # mail通知
    gmail=gmail_module(email, "到價通知")
    gmail.send_message(msg)
    return 0

scheduler=APScheduler()
# scheduler.add_job(id="task1", func=send_notification, trigger='interval', seconds=15) # for test
scheduler.add_job(id="task1", func=send_notification, trigger='cron', day_of_week='mon-fri', hour=13, minute=13) # 周一至周五早上9點(台灣時間)啟動function
# aws ec2的時間為台灣時間-8 h
scheduler.start()