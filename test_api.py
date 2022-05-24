import csv
import datetime
from FinMind.data import DataLoader

api = DataLoader()
# api.login_by_token(api_token='token')
# api.login(user_id='user_id',password='password')

df = api.taiwan_stock_daily(
    stock_id='Automobile',
    start_date='2022-04-02',
    end_date='2022-05-21'
)
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


# df = api.taiwan_stock_total_return_index(
#     index_id="TAIEX",
#     start_date='2022-05-02',
#     end_date='2022-05-21'
# )

# df = api.taiwan_stock_info()
# df.to_csv('test.csv',encoding='utf-8-sig')



# needs=["date", "stock_id", "year", "CashEarningsDistribution"]

# for col in df:
#     if col not in needs:
#         df=df.drop(columns=col)

print(df)

if df.empty:
    print("123")
else:
    print(456)



