import datetime
from flask_apscheduler import APScheduler
from api.finmind_module import fm
from api.api_aws import Aws_s3_api
from concurrent.futures import ThreadPoolExecutor, as_completed

timeString=datetime.datetime.now() + datetime.timedelta(hours=8) # AWS EC2，EC2的系統時間較台灣時間慢8小時
timeString=timeString.strftime("%Y_%m_%d") # AWS EC2，EC2的系統時間較台灣時間慢8小時
# timeString = datetime.datetime.now().strftime("%Y_%m_%d") # localhost


def update_cdn_TAIEX(): #每12小時自動更新一次TAIEX資料
    stock={
        "stock_transaction":[],
        "stock_data":None
    }
    stock_id="TAIEX"
    json_filename=stock_id+"-"+timeString+".json"
    s3=Aws_s3_api() # 將資料上傳至s3
    fm_sdk=fm(stock_id)
    stock["stock_transaction"]=fm_sdk.get_stock_transaction() # cdn無資料從finmind的api取得資料
    s3.upload_json_data(stock, json_filename)
    return 0

def update_cdn_top_stocks_news(): # 每8小時自動更新一次新聞資料
    top_stocks=["2330", "2317", "2454", "2412", "6505"] # 台股前五權值股
    threads=[]
    temp=[]
    s3=Aws_s3_api() 
    fm_sdk=fm(None)
    with ThreadPoolExecutor(max_workers=20) as executor: # 平行任務處理 ( 非同步 ) 的功能，能夠同時處理多個任務
        for stock in top_stocks:
            threads.append(executor.submit(fm_sdk.get_stock_news, stock))
        for task in as_completed(threads):
            temp.append(task.result())
            stock_data=task.result()
            if stock_data:
                json_filename=stock_data[0]["stock_id"]+"-"+"news"+timeString+".json"
                s3.upload_json_data(task.result(), json_filename)
    return 0

scheduler=APScheduler()
scheduler.add_job(id="update_task1", func=update_cdn_TAIEX, trigger='cron', day_of_week='mon-fri', hour=1) # 周一至周五早上9點(台灣時間)啟動function
scheduler.add_job(id="update_task2", func=update_cdn_TAIEX, trigger='cron', day_of_week='mon-fri', hour=10) # 周一至周五晚上6點(台灣時間)啟動function
scheduler.add_job(id="update_task3", func=update_cdn_top_stocks_news, trigger='interval', hours=8) # 每8小時更新一次五大權值股新聞
# aws ec2的時間為台灣時間-8 h
scheduler.start()