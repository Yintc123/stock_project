import urllib.request as req
import pandas as pd
import bs4
import time
from db import *

stock_id="2881" # 2330, 2454, 1101, 2317, 2412, 2881
stock_id=["2330", "2317", "2454", "2412", "6505", "1101"]

query_get_stock_id="SELECT stock_id FROM stock"
mycursor.execute(query_get_stock_id)
data=mycursor.fetchall()

query_get_stock_eps="SELECT*FROM stock_eps_roe WHERE stock_id=%s"

stock_list=[]
for stock in data:
    if stock[0] != "TAIEX":
        mycursor.execute(query_get_stock_eps, (stock[0], ))
        data=mycursor.fetchall()
        if data:
            continue
        stock_list.append(stock[0])

print(stock_list)

# for stock in stock_list:
#     stock_data={
#         "stock_id":stock,
#         "stock_name":None,
#         "stock_data":[]
#     }

#     url='https://goodinfo.tw/tw/StockBzPerformance.asp?STOCK_ID='+stock

#     request=req.Request(url, headers={
#         "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36"
#     })

#     with req.urlopen(request) as response:
#         data=response.read().decode('utf-8')

#     root=bs4.BeautifulSoup(data, 'html.parser')

#     if not root:
#         print("No data")
#         continue

#     table=root.find("table", id='tblDetail') # 選取特定table
#     rows=table.find_all('tr') # 選取table內的tr

#     stock_name=root.find("title")
#     stock_data["stock_name"]=stock_name.string.replace(" ", "").split(")")[1].split("歷")[0]
#     arr=[]
#     needs=[0, 16, 17, 18, 20] # 需要數據的index

#     for row in rows:
#         data=row.find_all("td") # 選取tr內的td
#         a1=[] # 創造一個list暫存數據
#         j=0
#         for value in data:
#             if j in needs:
#                 if value.text=="-" or value.text=="年度" or value.text=="收盤": # 當數據的值為-，即為此row數據不完全
#                     a1=[] # 清空a1
#                     break # 跳出此迴圈
#                 a1.append(value.text)
#             j+=1
        
#         if a1: # a1有數據，將a1數據加入arr中
#             arr.append(a1)

#     stock_data["stock_data"]=arr

#     for data in reversed(stock_data["stock_data"]): # 反轉列表從舊到新
#         print(data)
#         query="INSERT INTO stock_eps_roe (stock_id, year, ROE, ROA, EPS, BPS) VALUES(%s, %s, %s, %s, %s, %s)"
#         mycursor.execute(query, (stock_data["stock_id"], data[0], data[1], data[2], data[3], data[4]))
#         print("done!")
    
#     print(stock)
#     print("rest 10s")
    
#     # break
#     time.sleep(10)

#     mydb.commit()







# with open('test.txt', mode='w', encoding='utf-8') as file:
#     file.write(data)

# query_stock="SELECT*FROM stock_eps_roe WHERE year='22Q1' AND ROE='4.71(年估)' AND ROA='3.03(年估)'"
# mycursor.execute(query_stock)
# result=mycursor.fetchall()
# print(result)

# query_update="UPDATE stock set stock_id='4148' WHERE stock_id='4148      '"
# mycursor.execute(query_update)
# mydb.commit()
# print("done")

# query_delete="DELETE FROM stock_eps_roe WHERE stock_id='2454'"
# mycursor.execute(query_delete)
# mydb.commit()



# query_stock="SELECT*FROM stock_eps_roe WHERE stock_id='1234'"
# mycursor.execute(query_stock)
# result=mycursor.fetchall()
# print(result)