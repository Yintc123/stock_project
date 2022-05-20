from flask import *
from dotenv import *
from .finmind_module import fm
from data.stock_db import stock_info_db as stk_db

env='.env' # 執行環境
load_dotenv(override=True)

error={
        "error":True,
        "message":None
}

app_stock=Blueprint("api_stock", __name__)

@app_stock.route("/stocks/news", methods=["GET"])
def get_stocks_news():
    data={}
    fm_sdk=fm(None)
    data=fm_sdk.get_stock_news("2330")
    return data 

@app_stock.route("/stock/<stock_id>", methods=["GET"])
def get_stock(stock_id):
    stock={
        "stock_transaction":[],
        "stock_data":None
    }

    fm_sdk=fm(stock_id)
    stock["stock_transaction"]=fm_sdk.get_stock_transaction() # 將dataframe格式轉為dictionary
    stock["stock_data"]=fm_sdk.get_stock_data() # 將dataframe格式轉為dictionary
    stock["stock_data"].update(fm_sdk.get_stock_eps())
    stk=stk_db()
    data=stk.get_stock(stock_id)
    if data:
        data=data[0]
        stock["stock_data"].update({
            "ROE":data["ROE"],
            "stock_name":data["stock_name"]
        })

    return stock

@app_stock.route("/stock/<stock_id>/PER", methods=["GET"])
def get_stock_PER(stock_id):
    data={"stock_data":None}
    fm_sdk=fm(stock_id)
    data["stock_data"]=fm_sdk.get_stock_data_10days()
    return data

@app_stock.route("/stock/<stock_id>/EPS", methods=["GET"])
def get_stock_EPS(stock_id):
    data={"stock_data":None}
    stk=stk_db()
    d=stk.get_stock(stock_id)
    reversed_data=list(reversed(d)) # 反轉list使各回傳資料順序一致
    data["stock_data"]=reversed_data
    return data