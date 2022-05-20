from FinMind.data import DataLoader
import datetime
import requests
import pandas as pd

class fm():
    def __init__(self, stock_id):
        self.stock_id=stock_id
        self.fin_mind=DataLoader()

    def get_stock_transaction(self):
        df=self.fin_mind.taiwan_stock_daily(
            stock_id=self.stock_id,
            start_date='1990-01-01',
            end_date=datetime.date.today() # 今日日期
        )

        df.rename(columns={
            'max':'high',
            'min':'low',
            'date':'time'
        }, inplace=True)

        return df.to_dict('records') # 將dataframe格式轉為list

    def get_stock_data(self):
        try:
            df=self.fin_mind.taiwan_stock_per_pbr(
                stock_id=self.stock_id,
                start_date=datetime.date.today() - datetime.timedelta(days=1) # 今日未收盤，故無今日的per值，需使用昨日日期
            )

            df.rename(columns={
                'dividend_yield':'dividend-yield',
            }, inplace=True)
            
            return df.to_dict('records')[0] # 將dataframe格式轉為dictionary
        except:
            print("error in get_stock_data()")
            return {"data":None}

    def get_stock_data_10days(self):
        try:
            df=self.fin_mind.taiwan_stock_per_pbr(
                stock_id=self.stock_id,
                start_date=datetime.date.today() - datetime.timedelta(days=10) # 今日未收盤，故無今日的per值，需使用昨日日期
            )

            df.rename(columns={
                'dividend_yield':'dividend-yield',
            }, inplace=True)
            
            return df.to_dict('index') # 將dataframe格式以index為key轉為dictionary
        except:
            print("error in get_stock_data_10days()")
            return {"data":None}


    def get_stock_eps(self):
        try:
            url = "https://api.finmindtrade.com/api/v4/data"
            parameter = {
                "dataset": "TaiwanStockFinancialStatements",
                "data_id": self.stock_id,
                "start_date": datetime.date.today() - datetime.timedelta(days=365),
                "token": "", # 參考登入，獲取金鑰
            }
            data = requests.get(url, params=parameter)
            data = data.json()
            data = pd.DataFrame(data['data'])
            types=data["type"]
            
            for param in types:
                if param != "EPS": # 將type非EPS的row刪除
                    data.drop(data[types==param].index, inplace=True)
            eps=round(self.calculate_eps(data.to_dict('records')), 2) # 取小數點後第二位
            return {"EPS":eps}
        except:
            print("error in get_stock_eps()")
            return {"data":None}

    def get_stock_news(self, stock_id):
        url = "https://api.finmindtrade.com/api/v4/data"
        parameter = {
            "dataset": "TaiwanStockNews",
            "data_id":stock_id,
            "start_date": datetime.date.today() - datetime.timedelta(days=3),
            "end_date": datetime.date.today(),
            "token": "", # 參考登入，獲取金鑰
        }
        data = requests.get(url, params=parameter)
        data = data.json()
        data = pd.DataFrame(data['data'])
        d=data.to_dict('records')
        d1=self.arrange_news(d)
        return d1

    def calculate_eps(self, data):
        sum=0
        for index in data:
            sum+=index["value"]
        return sum

    def arrange_news(self, list_news):
        data={
            "source":[],
            "news_data":{}
        }

        for news in list_news:
            if news["source"] not in data["source"]:
                data["source"].append(news["source"])
                data["news_data"][news["source"]]=[]
            data["news_data"][news["source"]].append(news)
        return data