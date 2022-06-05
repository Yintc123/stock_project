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
    stock["stock_transaction"]=fm_sdk.get_stock_transaction()
    if not stock["stock_transaction"]:
        error["message"]="無此股票資訊"
        return error

    if stock_id !="TAIEX":
        stock["stock_data"]=get_last_data_from_dict(fm_sdk.get_stock_data(7))
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
    data["stock_data"]=fm_sdk.get_stock_data(10)
    return data

@app_stock.route("/stock/<stock_id>/EPS", methods=["GET"])
def get_stock_EPS(stock_id):
    data={"stock_data":None}
    stk=stk_db()
    d=stk.get_stock(stock_id)
    reversed_data=list(reversed(d)) # 反轉list使各回傳資料順序一致
    data["stock_data"]=reversed_data
    return data

def get_last_data_from_dict(data):
     # df.to_dict('index')是將資料以index作為key的dict，但dict的資料無順序性，如要取最新的一筆資料須得到最大的index值
    return data[len(data)-1]