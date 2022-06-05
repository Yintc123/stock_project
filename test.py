import urllib.request as req
import pandas as pd
import bs4

url='https://goodinfo.tw/tw/StockBzPerformance.asp?STOCK_ID=2330'

request=req.Request(url, headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36"
})

with req.urlopen(request) as response:
    data=response.read().decode('utf-8')

# with open('test.txt', mode='w', encoding='utf-8') as file:
#     file.write(data)

root=bs4.BeautifulSoup(data, 'html.parser')
table=root.find("table", id='tblDetail')
title=table.find_all('tr')

arr=[]
needs=[0, 16, 17, 18, 20]

for i in title:
    value=i.find_all("td")
    a1=[]
    j=0
    for v in value:
        if j in needs:
            if v.text=="-":
                a1=[]
                break
            a1.append(v.text)
        j+=1
    
    if a1:
        arr.append(a1)

print(arr)


