import urllib.request as req
import pandas as pd
import bs4
import time
from db import *

stock_id="2881" # 2330, 2454, 1101, 2317, 2412, 2881

stock_data={
    "stock_id":stock_id,
    "stock_name":None,
    "stock_data":[]
}

url='https://goodinfo.tw/tw/StockBzPerformance.asp?STOCK_ID='+stock_id

request=req.Request(url, headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36"
})

with req.urlopen(request) as response:
    data=response.read().decode('utf-8')

root=bs4.BeautifulSoup(data, 'html.parser')
table=root.find("table", id='tblDetail') # 選取特定table
rows=table.find_all('tr') # 選取table內的tr

stock_name=root.find("title")
stock_data["stock_name"]=stock_name.string.replace(" ", "").split(")")[1].split("歷")[0]
arr=[]
needs=[0, 16, 17, 18, 20] # 需要數據的index

for row in rows:
    data=row.find_all("td") # 選取tr內的td
    a1=[] # 創造一個list暫存數據
    j=0
    for value in data:
        if j in needs:
            if value.text=="-" or value.text=="年度" or value.text=="收盤": # 當數據的值為-，即為此row數據不完全
                a1=[] # 清空a1
                break # 跳出此迴圈
            a1.append(value.text)
        j+=1
    
    if a1: # a1有數據，將a1數據加入arr中
        arr.append(a1)

stock_data["stock_data"]=arr
# print(stock_data)

for data in stock_data["stock_data"]:
    print(data)
    query="INSERT INTO stock_info (stock_name, stock_id, year, ROE, ROA, EPS, BPS) VALUES(%s, %s, %s, %s, %s, %s, %s)"
    mycursor.execute(query, (stock_data["stock_name"], stock_data["stock_id"], data[0], data[1], data[2], data[3], data[4]))
    print("done!")

mydb.commit()

# with open('test.txt', mode='w', encoding='utf-8') as file:
#     file.write(data)