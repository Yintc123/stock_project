from flask import *
from dotenv import *
import pandas as pd
from FinMind.data import DataLoader

env='.env' # 執行環境
load_dotenv(override=True)

error={
        "error":True,
        "message":None
}

app_stock=Blueprint("api_stock", __name__)

@app_stock.route("/stock", methods=["GET"])
def get_stock():
    stock={
        "stock_id":None,
        "stock_data":[]
    }
    needs=["date", "open", "max", "min", "close"]
    fin_mind=DataLoader()
    df=fin_mind.taiwan_stock_daily(
        stock_id='0050',
        start_date='2022-04-02',
        end_date='2022-04-30'
    )
    stock["stock_id"]=df["stock_id"][0]
    for col in df:
        if col not in needs: # 去除不必要的欄位
            df=df.drop(columns=col)
    stock["stock_data"]=df.to_dict('records') # 將dataframe格式轉為dictionary
    return stock