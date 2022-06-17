import urllib.request as req
import pandas as pd
import bs4
import time
from db import *

# 上櫃

url='https://isin.twse.com.tw/isin/C_public.jsp?strMode=4'

request=req.Request(url, headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36"
})

with req.urlopen(request) as response:
    # data=response.read().decode('utf-8')
    # data=response.read().decode('big5')
    data=response.read().decode('cp950')

root=bs4.BeautifulSoup(data, 'html.parser')
table=root.find("table", class_="h4") # 選取特定table
rows=table.find_all('tr') # 選取table內的tr
b=table.find_all("b")
stock_list=[]
no_needs_index=[1, 2, 5 ,6]

for row in rows:
    stock_data={
            "stock_id":None,
            "stock_name":None,
            "listed":None,
            "industry":None
        }
    # if row.find("b"):
    #     print(row.find("b").text)
    #     if row.find("b").text == "股票":
    #         continue
    if not row.find_all("td"):
        continue
    tds=row.find_all("td")
    for index in range(0, len(tds)):
        if index in no_needs_index:
            continue
        # if tds[index].text =='有價證券代號及名稱 ':
        #     break
        if index==0:
            comp=tds[index].text
            comp=comp.split("　")
            if len(comp[0])>4:
                break
            stock_data["stock_id"]=comp[0]
            stock_data["stock_name"]=comp[1]
        if index==3:
            stock_data["listed"]=tds[index].text
        if index==4:
            stock_data["industry"]=tds[index].text
    if not stock_data["stock_id"]:
        continue
    stock_list.append(stock_data)    

for stock in stock_list:
    print(stock)
    query_get="SELECT*FROM stock WHERE stock_id=%s"
    mycursor.execute(query_get, (stock["stock_id"], ))
    data=mycursor.fetchone()
    if data: 
        query_update="UPDATE stock set stock_name=%s, listed=%s, industry=%s WHERE stock_id=%s"
        mycursor.execute(query_update, (stock["stock_name"], stock["listed"], stock["industry"], stock["stock_id"]))
        print("{}更新完成".format(stock["stock_id"]))
        continue

    query_insert="INSERT INTO stock (stock_id, stock_name, listed, industry) VALUES(%s, %s, %s, %s)"
    mycursor.execute(query_insert, (stock["stock_id"], stock["stock_name"], stock["listed"], stock["industry"]))
    print("done!")

mydb.commit()


# with open('test.txt', mode='w', encoding='utf-8') as file:
#     file.write(data)

# query_stock="SELECT*FROM stock WHERE stock_id='2330'"
# mycursor.execute(query_stock)
# result=mycursor.fetchall()
# print(result)