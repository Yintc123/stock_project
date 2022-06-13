from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from flask import *
from dotenv import *
import jwt
from .finmind_module import fm
from data.stock_db import stock_info_db as stk_db

env='.env' # 執行環境
load_dotenv(override=True)

error={
        "error":True,
        "message":None
}

member_key=dotenv_values(env)["member_key"] # jwt_key

app_stock=Blueprint("api_stock", __name__)

@app_stock.route("/stocks/news", methods=["GET"])
def get_stocks_news():
    start=time.time()
    print("news starts")
    stock_id=["2330", "2317", "2454", "2412", "6505"] # 台股前五權值股
    token_member=request.cookies.get("token_member") # 判斷是否登入
    if token_member:
        payload_member=jwt.decode(token_member, member_key, algorithms="HS256")
        stock_id=get_stock_id_from_token(payload_member["data"]["favorite"])

    data={}
    temp=[]
    threads=[]
    fm_sdk=fm(None)
    with ThreadPoolExecutor(max_workers=20) as executor: # 平行任務處理 ( 非同步 ) 的功能，能夠同時處理多個任務
        for stock in stock_id:
            threads.append(executor.submit(fm_sdk.get_stock_news, stock))
        for task in as_completed(threads):
            temp.append(task.result())

    data=arrange_news(temp)
    end=time.time()
    print("get_stock_news執行時間：", (end-start))
    return data 

@app_stock.route("/stock/<stock_id>", methods=["GET"])
def get_stock(stock_id):
    start=time.time()
    print("stock starts")
    stock={
        "stock_transaction":[],
        "stock_data":None
    }

    fm_sdk=fm(stock_id)
    stk=stk_db()

    stock["stock_transaction"]=fm_sdk.get_stock_transaction()

    if not stock["stock_transaction"]:
        error["message"]="無此股票資訊"
        return error
    if stock_id !="TAIEX":
        stock["stock_data"]=get_last_data_from_dict(fm_sdk.get_stock_data(7))
        stock["stock_data"].update(fm_sdk.get_stock_eps())

        stock_data=stk.get_stock(stock_id)
        eps_roe=get_last_data_from_dict(stk.get_eps_roe(stock_id))
        if stock_data:
            stock["stock_data"].update({
                "ROE":eps_roe["ROE"],
                "stock_name":stock_data["stock_name"]
            })

    end=time.time()
    print("get_stock執行時間：", (end-start))
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
    stock_eps_roe=stk.get_eps_roe(stock_id)
    data["stock_data"]=stock_eps_roe
    return data

def get_last_data_from_dict(data):    
    return data[len(data)-1] # df.to_dict('index')是將資料以index作為key的dict，但dict的資料無順序性，如要取最新的一筆資料須得到最大的index值


def get_stock_id_from_token(favorite_list):
    stock_list=[]
    if not favorite_list:
        stock_list=["2330", "2317", "2454", "2412", "6505"]
        return stock_list
    for favorite in favorite_list:
        stock_list.append(favorite["stock_id"])
    return stock_list

def arrange_news(list_news):
    data={
        "source":[],
        "news_data":{}
    }
    for stock in list_news:
        if not stock:
            continue
        for news in stock:
            news_source=rename_news_source(news["source"])
            if news_source not in data["source"]:    
                data["source"].append(news_source)
                data["news_data"][news_source]=[]
            if is_in_list(news_source, news["link"], news["title"], data["news_data"][news_source]): # 跳過重複的新問
                continue
            data["news_data"][news_source].append(news)
    return data

def is_in_list(news_source, news_link, news_title, dict_list):
    for item in dict_list:
        if news_link == item["link"]:
            return True
        if news_title == item["title"]:
            return True
        if news_source == "Anue鉅亨":
            if news_link.split("/")[-1] == item["link"].split("/")[-1]:
                return True
    return False

def rename_news_source(news_source):
    source_list={
        "鉅亨新聞":"Anue鉅亨",
        "鉅亨網":"Anue鉅亨",
        "Yahoo奇摩新聞":"Yahoo奇摩股市",
        "Apple Daily TW":"蘋果新聞網",
    }
    if news_source in source_list:
        return source_list[news_source]
    return news_source