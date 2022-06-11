import data.connection_pool as db

class stock_info_db():
    def __init__(self):
        self.conn=None
        self.cur=None

    def connection(self):
        try:
            self.conn=db.conn_pool.get_connection()
            self.cur=self.conn.cursor(dictionary=True) # cursor return dictionary
            print("successful access to the connection")
        except:
            print("error in the connection")

    def close(self):
        try:
            self.cur.close() # cursor.close()釋放從資料庫取得的資源，兩個皆須關閉
            self.conn.close() # connection.close()方法可關閉對連線池的連線，並釋放相關資源
            print("close the connection successfully")
        except:
            print("error in closing the connection")

    def get_stock(self, stock_id):
        try:
            # query="SELECT*FROM stock_info WHERE stock_id=%s"
            query="SELECT*FROM stock WHERE stock_id=%s"
            self.connection()
            self.cur.execute(query %stock_id)
            data=self.cur.fetchone()
            self.close()
            return data
        except:
            self.close() # 出現error直接關閉連線，避免佔用資料庫資源
            print("error in function, get_stock()")
            return None
    
    def get_eps_roe(self, stock_id):
        try:
            # query="SELECT*FROM stock_info WHERE stock_id=%s"
            query="SELECT*FROM stock_eps_roe WHERE stock_id=%s"
            self.connection()
            self.cur.execute(query %stock_id)
            data=self.cur.fetchall()
            self.close()
            return data
        except:
            self.close() # 出現error直接關閉連線，避免佔用資料庫資源
            print("error in function, get_stock()")
            return None


    def new_get_stock_history(self, stock_id):
        try:
            query="SELECT*FROM stock_history WHERE stock_id=%s"
            self.connection()
            self.cur.execute(query %stock_id)
            data=self.cur.fetchall()
            self.close()
            return data
        except:
            self.close() # 出現error直接關閉連線，避免佔用資料庫資源
            print("error in function, get_stock()")
            return None

    def get_stock_name(self, stock_id):
            query="SELECT*FROM stock WHERE stock_id=%s"
            self.connection()
            self.cur.execute(query %stock_id)
            data=self.cur.fetchone()
            self.close()
            return data