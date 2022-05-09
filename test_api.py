from FinMind.data import DataLoader

api = DataLoader()
# api.login_by_token(api_token='token')
# api.login(user_id='user_id',password='password')

df = api.taiwan_stock_daily(
    stock_id='0050',
    start_date='2022-04-02',
    end_date='2022-04-30'
)
# print(df)
# print(df["stock_id"])

for i in df:
    for j in df[i]:
        print(j)