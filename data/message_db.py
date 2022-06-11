import data.connection_pool as db
import mysql.connector

class message_db():
    def __init__(self):
        self.conn=None
        self.cur=None

    def connection(self):
        try:
            self.conn=db.conn_pool.get_connection()
            self.cur=self.conn.cursor(dictionary=True) # cursor return dictionary
            print("successful access to the connection.")
        except:
            print("error in the connection.")

    def close(self):
        try:
            self.cur.close() # cursor.close()釋放從資料庫取得的資源，兩個皆須關閉
            self.conn.close() # connection.close()方法可關閉對連線池的連線，並釋放相關資源
            print("close the connection successfully.")
        except:
            print("error in closing the connection.")

    def get_message(self, stock_id):
        query_get_message="SELECT*FROM message_board WHERE stock_id=\'%s\'" # stock_id的資料格式為VARCHAR(255)，需要使用跳脫符號\ 
        self.connection()
        self.cur.execute(query_get_message %stock_id)
        stock_message=self.cur.fetchall()
        self.close()
        print("Success in get_message.")
        return stock_message

    def add_message(self, user_id, stock_id, message):
        query_add_message="INSERT INTO message_board (user_id, stock_id, message) VALUES(%s, %s, %s)" # stock_id的資料格式為VARCHAR(255)，需要使用跳脫符號\ 
        self.connection()
        self.cur.execute(query_add_message, (user_id, stock_id, message))
        self.conn.commit()
        self.close()
        print("Success in add_message.")
        return self.response_text(0, "留言成功")

    def delete_message(self, stock_id):
        query_delete_message="DELETE FROM message_board WHERE stock_id=\'%s\'"
        self.connection()
        self.cur.execute(query_delete_message %stock_id)
        self.conn.commit()
        self.close()
        print("Success in get_favorite_stock.")
        return self.response_text(0, "刪除成功")

    def response_text(self, status, message):
        resp={
            "error":None,
            "message":None
        }
        if status==0:
            resp["error"]=False
        else:
            resp["error"]=True
        resp["message"]=message
        return resp