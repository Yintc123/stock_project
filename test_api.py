import csv
import datetime
from FinMind.data import DataLoader

api = DataLoader()
# api.login_by_token(api_token='token')
# api.login(user_id='user_id',password='password')

# df = api.taiwan_stock_daily(
#     stock_id='0050',
#     start_date='2022-04-02',
#     end_date='2022-04-30'
# )
# # print(df)
# # print(df["stock_id"])

# for i in df:
#     for j in df[i]:
#         print(j)

# df = api.taiwan_stock_dividend(
#     stock_id="2884",
#     start_date='2019-03-31',
# )

# df = api.taiwan_stock_per_pbr(
#     stock_id='2330',
#     start_date=datetime.date.today() - datetime.timedelta(days=365)
# )
# print(datetime.date.today() - datetime.timedelta(days=365))
# date=str(datetime.date.today() - datetime.timedelta(days=365))
# df = api.taiwan_stock_financial_statement(
#     stock_id="2330",
#     start_date=date,
# )


# df = api.taiwan_stock_info()
# df.to_csv('test.csv',encoding='utf-8-sig')



# needs=["date", "stock_id", "year", "CashEarningsDistribution"]

# for col in df:
#     if col not in needs:
#         df=df.drop(columns=col)

# print(df)

# if df.empty:
#     print("123")
# else:
#     print(456)



import requests
import pandas as pd
url = "https://api.finmindtrade.com/api/v4/data"
parameter = {
    "dataset": "TaiwanStockNews",
    "data_id":"2454",
    "start_date": "2022-05-20",
    # "end_date": "2022-04-03",
    "token": "", # 參考登入，獲取金鑰
}
data = requests.get(url, params=parameter)
data = data.json()
data = pd.DataFrame(data['data'])
print(data.head())

data.to_csv('test_new2.csv',encoding='utf-8-sig')
