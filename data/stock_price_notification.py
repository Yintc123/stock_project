import random
from data.member_db import member_db
from api.email_module import *


def test():
    print("test")

def send_notification():
    mb_db=member_db()
    favorite=mb_db.get_all_favorite_stock()
    for stock in favorite:
        if not stock["price"]:
            print("未設定到價通知")
            continue
        fake_price=get_fake_stock_price(stock["price"])
        if fake_price==stock["price"]:
            print("到價通知")
            member_info=mb_db.get_member(None, stock["user_id"])
            gmail=gmail_module(member_info["email"], "到價通知")
            msg="已達到您設定的價格"+str(fake_price)
            gmail.send_message(msg)
        print(fake_price)
    
    return 

def get_fake_stock_price(price):
    fake_price=price+round(random.uniform(-price/10000, price/10000), 1)
    return fake_price