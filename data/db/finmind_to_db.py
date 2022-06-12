import datetime
import json
import time
import pandas as pd

import requests
from db import *
from FinMind.data import DataLoader

# stock_id=["2330", "2317", "2454", "2412", "6505", "1101", "TAIEX"]
# needs=["stock_id", "open", "low", "high", "close", "volume", "time", "PER", "dividend_yield", "PBR"]
# query="INSERT INTO stock_history (stock_id, open, low, high, close, volume, time) VALUES(%s, %s, %s, %s, %s, %s, %s)"

# stocks={
#     "TAIEX":"台灣加權股票指數",
#     "2330":"台積電",
#     "2317":"鴻海",
#     "2454":"聯發科",
#     "2412":"中華電",
#     "6505":"台塑化",
#     "1101":"台泥"
#     }

# query_stock="INSERT INTO stock (stock_id, stock_name) VALUES(%s, %s)"
# for stock in stocks:
#     mycursor.execute(query_stock, (stock, stocks[stock]))
#     print("done!")
# mydb.commit()

# query_stock="SELECT*FROM stock_history WHERE stock_id='1101'"
# mycursor.execute(query_stock)
# result=mycursor.fetchall()
# print(result)

# 歷史股價
# api = DataLoader()
# # # api.login_by_token(api_token='token')
# # # api.login(user_id='user_id',password='password')

# for stock in stock_id:
#     if stock != "TAIEX":
#         continue
#     df = api.taiwan_stock_daily(
#         stock_id=stock,
#         start_date='1990-01-01',
#         end_date=datetime.date.today(), # 今日日期
#     )

#     df.rename(columns={
#         'max':'high',
#         'min':'low',
#         'Trading_Volume':'volume',
#         'date':'time'
#     }, inplace=True)

#     df=df.to_dict('records')

#     for row in df:
#         for key in list(row.keys()): # for key in row:迴圈中無法刪除key-value
#             if key not in needs:
#                 # print(key)
#                 row.pop(key)
#         mycursor.execute(query, (row[needs[0]], row[needs[1]], row[needs[2]], row[needs[3]], row[needs[4]], row[needs[5]], row[needs[6]]))
#         print(row)
#         print("done!")

# mydb.commit()

# 歷史"PER", "dividend_yield", "PBR"

# stock_id=["2330", "2317", "2454", "2412", "6505", "1101"]
# needs=["stock_id", "open", "low", "high", "close", "volume", "time", "PER", "dividend_yield", "PBR"]
# query="UPDATE stock_history set PER=%s, dividend_yield=%s, PBR=%s WHERE stock_id=%s AND time=%s"

# api = DataLoader()
# # api.login_by_token(api_token='token')
# # api.login(user_id='user_id',password='password')

# for stock in stock_id:
#     if stock=="2330":
#         continue
#     df = api.taiwan_stock_per_pbr(
#             stock_id=stock,
#             start_date='1990-01-01',
#             end_date=datetime.date.today(), # 今日日期
#         )

#     df.rename(columns={
#             'date':'time'
#         }, inplace=True)

#     df=df.to_dict('records')

#     for row in df:
#             for key in list(row.keys()): # for key in row:迴圈中無法刪除key-value
#                 if key not in needs:
#                     # print(key)
#                     row.pop(key)
#             mycursor.execute(query, (row[needs[7]], row[needs[8]], row[needs[9]], row[needs[0]], row[needs[6]]))
#             print(row)
#             print("done!")

# mydb.commit()


# 歷史資料

stock="TAIEX"

# api=DataLoader()

# df=api.taiwan_stock_daily(
#             stock_id=stock,
#             start_date='1990-01-01',
#             end_date=datetime.date.today(), # 今日日期
#         )
# df.rename(columns={
#             'max':'high',
#             'min':'low',
#             'date':'time'
#         }, inplace=True)
# # print(df.to_dict('records'))
# data_json=json.dumps(df.to_dict('records'))
# print(type(data_json))

# query="INSERT INTO stock_history (stock_id, stock_json) VALUES(%s, %s)"
# mycursor.execute(query, (stock, data_json))
# mydb.commit()

query="SELECT*FROM stock_history WHERE stock_id='TAIEX'"
mycursor.execute(query)
data=mycursor.fetchone()
data["time"]=data["time"]+datetime.timedelta(hours=8) 
print(data["time"])
print(datetime.datetime.today())
print(data["time"].strftime("%Y/%m/%d"))
print(datetime.datetime.today().strftime("%Y/%m/%d"))
print(data["time"].strftime("%Y/%m/%d")==datetime.datetime.today().strftime("%Y/%m/%d"))



# df=api.taiwan_stock_per_pbr(
#                 stock_id="2330",
#                 start_date= datetime.date.today() - datetime.timedelta(days=period), # 今日未收盤，故無今日的per值，需使用昨日日期
#             )

# df.rename(columns={
#     'dividend_yield':'dividend-yield',
# }, inplace=True)