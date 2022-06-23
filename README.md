# stock_project 台灣股票資訊

## 網址
https://yin888.info/

## 簡介
提供大盤及各股的基本資訊和基本的技術分析指標以協助判斷投資的股票標的，首頁提供前五權值股近 3 日的相關新聞。註冊會員系統並關注各股可以使用到價通知的功能，首頁也會顯示關注各股近 3 日的相關新聞。

## 功能
*  訪客
    *   移動平均線
        *   10 日線
            <br/>短期趨勢判斷。
        *   月線
            <br/>中期趨勢判斷。
        *   年線
            <br/>長期趨勢判斷。
    *   各股資訊
        *   本益比
            <br/>股價和近 4 季收益的比例，用於衡量一家公司的價值。公司收益提供近 10 日的本益比。
        *   現金殖利率
            <br/>近 4 季現金股利和股價的比例，投資的報酬率。提供近 10 日的現金殖利率。
        *   股價淨值比
            <br/>股價和每股淨值的比例，用於衡量一家公司的價值。提供近 10 日的股價淨值比。
        *   近 4 季 EPS
            <br/>每股盈餘。提供歷年 EPS 。
        *   ROE ( % )
            <br/>股東權益報酬率，一家公司運用自有資本的獲利效率。提供歷年 ROE 。
*  會員
    *   各股關注
        *   到價通知
            *   email
                <br/>當股價觸及目標股價，寄送 email 通知會員。(需驗證 email )
            *   網頁推播
                <br/>當股價觸及目標股價，網頁推播通知會員。(需訂閱推播通知)
        *   新聞
            <br/>首頁呈現關注各股近3日的新聞。
    *   各股留言板
        <br/>分享對於各股的看法。

## 網頁架構
![pic_web_framework](readme_pictures/web_framework.png)

#### 資料獲取流程圖
<img src="readme_pictures/process_chart.png" width="500px">

## 使用工具
*   AWS
    *   EC2
    *   RDS
    *   S3
    *   CloudFront
*   Python
    *   flask
    *   FinMind
    *   twstock
    *   jwt
    *   boto3
    *   pandas
    *   smtplib
    *   concurrent.futures
    *   pywebpush
    *   flask_apscheduler
    *   dotenv
    *   mysql.connector.pooling
*   JavaScript
    *   TradingView
    *   Service Workers
*   Others
    *   Docker
    *   nginx
    *   git

## 問題解決
### 發生問題：網頁讀取速度過久(首頁約需15秒的讀取時間)
### 尋找真因：
*   大盤歷史股價及成交量數據量過大(透過api送出需求至回傳時間約需 1.5 秒)
*   各股新聞(透過api送出需求至回傳時間約需 1-3 秒不等，依各股新聞數量決定)
### 解決方案：
- [ ] Local storage
    * 將資料儲存至本機端
    * 提升個人瀏覽器的存取速度
    * 無法即時更新資料
    * 容量僅約 5 MB
- [X] AWS S3
    * 透過 AWS CloudFront 將資料緩存至 CDN 提供商位於全球各地的多個伺服器節點
    * 提升所有requests的存取速度
    * 即時更新資料

避免使用者等待讀取時間過久以及確保使用者能得到最新資訊，於每日的 9 點及 18 點自動更新大盤的股價資訊確保資料為最新的資訊；每 8 小時自動更新台股五大權值股的新聞。
