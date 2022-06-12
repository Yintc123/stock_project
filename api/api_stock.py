from threading import Thread
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
    stock_id=["2330", "2317", "2454", "2412", "6505"] # ["2330", "2317", "2454", "2412", "6505"]
    token_member=request.cookies.get("token_member") # 判斷是否登入
    if token_member:
        payload_member=jwt.decode(token_member, member_key, algorithms="HS256")
        stock_id=get_stock_id_from_token(payload_member["data"]["favorite"])

    data={}
    temp=[]
    threads=[]
    i=0
    fm_sdk=fm(None)
    with ThreadPoolExecutor(max_workers=20) as executor:
        for stock in stock_id:
            t_start=time.time()
            # temp+=fm_sdk.get_stock_news(stock)
            # thread = CustomThread(fm_sdk.get_stock_news(stock))
            # threads.append(thread)
            # thread.start()
            threads.append(executor.submit(fm_sdk.get_stock_news, stock))
            t_end=time.time()
            print(stock)
            print("news執行時間：", (t_end-t_start))
            i+=1
        
        for task in as_completed(threads):
            temp.append(task.result())
            # print(task.result())
    
    # for thread in threads:
    #     thread.join()
    #     news_data = thread.value
    #     temp.append(news_data)

    # print(temp)

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

    start=time.time()
    # print("finmind_stock starts")
    stock["stock_transaction"]=fm_sdk.get_stock_transaction()
    end=time.time()
    # print("finmind執行時間：", (end-start))

    # start=time.time()
    # print("db starts")
    # stock["stock_transaction"]=stk.new_get_stock_history("TAIEX")
    # stock["stock_transaction"]=json.dumps(stock["stock_transaction"]["stock_json"])
    # end=time.time()
    # print("db執行時間：", (end-start))
    # print(stock["stock_transaction"])

    # stock["stock_transaction"]=stk.new_get_stock_history(stock_id)
    if not stock["stock_transaction"]:
        error["message"]="無此股票資訊"
        return error
    # print(stock["stock_transaction"])
    if stock_id !="TAIEX":
        stock["stock_data"]=get_last_data_from_dict(fm_sdk.get_stock_data(7))
        stock["stock_data"].update(fm_sdk.get_stock_eps())
        # stock["stock_data"]=fm_sdk.get_stock_eps()

        # last_transaction_data=len(stock["stock_transaction"])-1
        stock_data=stk.get_stock(stock_id)
        eps_roe=get_last_data_from_dict(stk.get_eps_roe(stock_id))
        print(eps_roe)
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
     # df.to_dict('index')是將資料以index作為key的dict，但dict的資料無順序性，如要取最新的一筆資料須得到最大的index值
    return data[len(data)-1]


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
            if news["source"] not in data["source"]:
                data["source"].append(news["source"])
                data["news_data"][news["source"]]=[]
            if is_in_list(news["link"], data["news_data"][news["source"]]):
                continue
            data["news_data"][news["source"]].append(news)
    return data

def is_in_list(value, dict_list):
    for item in dict_list:
        if value == item["link"]:
            return True
    return False


# custom thread
class CustomThread(Thread):
    # constructor
    def __init__(self, func):
        # execute the base constructor
        Thread.__init__(self)
        # set a default value
        self.value = None
        self.func=func
 
    # function executed in a new thread
    def run(self):
        # block for a moment
        # sleep(1)
        
        # store data in an instance variable
        # self.value = 'Hello from a new thread'
        self.value = self.func
