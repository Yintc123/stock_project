import data.connection_pool as db
import mysql.connector

class member_db():
    def __init__(self):
        self.conn=None
        self.cur=None

    def connection(self):
        try:
            self.conn=db.conn_pool.get_connection()
            self.cur=self.conn.cursor(dictionary=True) # cursor return dictionary
            # print("successful access to the connection.")
        except:
            # print("error in the connection.")
            return

    def close(self):
        try:
            self.cur.close() # cursor.close()釋放從資料庫取得的資源，兩個皆須關閉
            self.conn.close() # connection.close()方法可關閉對連線池的連線，並釋放相關資源
            # print("close the connection successfully.")
        except:
            # print("error in closing the connection.")
            return

    def create_member(self, username, email, password):
        try:
            query_create_member="INSERT INTO member (username, email, password) VALUES(%s, %s, %s)"
            self.connection()
            self.cur.execute(query_create_member, (username, email, password))
            self.conn.commit()
            self.close()
            # print("Success in create_member.")
            return self.response_text(0, "註冊成功")
        except:
            self.close()
            # print("error in create_member.")
            message="500 internal database error."
            # return self.response_text(1, message)

    def get_member(self, email, id):
        try:
            column=None
            query_get_member=None
            if email:
                column=email
                query_get_member="SELECT*FROM member WHERE email=\'%s\'" # email的資料格式為VARCHAR(255)，需要使用跳脫符號\ 
            else:
                column=id
                query_get_member="SELECT*FROM member WHERE id=%s"
            self.connection()
            self.cur.execute(query_get_member %column)
            member_info=self.cur.fetchone()
            self.close()
            # print("Success in get_member.")
            return member_info 
        except:
            self.close()
            # print("error in get_member.")
            message="500 internal database error."
            return self.response_text(1, message)

    def renew_member(self, user_id, username, email, password, photo, email_status):
        try:
            member_info={
                "email":email,
                "username":username,
                "password":password,
                "photo":photo,
                "email_status":email_status
            }

            for info in member_info:
                if member_info[info]=='null':
                    member_info[info]=None
            
            query_renew_member="UPDATE member set {}=%s WHERE id="+user_id

            self.connection()
            for info in member_info:
                if not member_info[info]:
                    continue
                if info=="email":
                    result=self.get_member(email, None) # 確定email無人註冊
                    if result and result["id"] != int(user_id):
                        return self.response_text(1, "email已被註冊")
                    self.connection() # get_member()將所有connection和cursor關閉
                self.cur.execute(query_renew_member.format(self.escape_column_name(info)), (member_info[info],))
            self.conn.commit()
            self.close()        
            return self.response_text(0, "會員資訊更新成功")
        except:
            self.close()
            print("error in renew_member.")
            message="500 internal database error."
            return self.response_text(1, message)

    def add_push_token(self, user_id, token):
        try:
            query_add_price="UPDATE member set push_token=%s WHERE id=%s"
            self.connection()
            self.cur.execute(query_add_price, (token, user_id))
            self.conn.commit()
            self.close()
            # print("Success in add_push_token.")
            return self.response_text(0, "token紀錄完成")
        except:
            self.close()
            # print("error in add_push_token.")
            message="500 internal database error."
            return self.response_text(1, message)

    def get_favorite_stock(self, user_id):
        try:
            query_get_favorite="SELECT stock_id, price FROM favorite WHERE user_id=%s"
            self.connection()
            self.cur.execute(query_get_favorite, (user_id,))
            favorite=self.cur.fetchall()
            self.close()
            # print("Success in get_favorite_stock.")
            return favorite          
        except:
            self.close()
            # print("error in get_favorite_stock.")
            message="500 internal database error."
            return self.response_text(1, message)

    def add_favorite_stock(self, user_id, stock_id):
        try:
            favorite=self.get_favorite_stock(user_id)
            for dict in favorite:
                if dict["stock_id"]==int(stock_id):
                    return self.response_text(0, "已添加成功")
            query_add_favorite="INSERT INTO favorite (user_id, stock_id) VALUES(%s, %s)"
            self.connection()
            self.cur.execute(query_add_favorite, (user_id, stock_id))
            self.conn.commit()
            self.close()
            # print("Success in add_favorite_stock.")
            return self.response_text(0, "添加成功")
        except:
            self.close()
            # print("error in add_favorite_stock.")
            message="500 internal database error."
            return self.response_text(1, message)

    def delete_favorite_stock(self, user_id, stock_id):
        try:
            query_get_favorite="DELETE FROM favorite WHERE user_id=%s AND stock_id=%s"
            self.connection()
            self.cur.execute(query_get_favorite, (user_id, stock_id))
            self.conn.commit()
            self.close()
            # print("Success in get_favorite_stock.")
            return self.response_text(0, "刪除成功")
        except:
            self.close()
            # print("error in delete_favorite_stock.")
            message="500 internal database error."
            return self.response_text(1, message)

    def add_favorite_stock_price(self, user_id, stock_id, price):
        try:
            query_add_price="UPDATE favorite set price=%s WHERE user_id=%s AND stock_id=%s"
            self.connection()
            self.cur.execute(query_add_price, (price, user_id, stock_id))
            self.conn.commit()
            self.close()
            # print("Success in add_favorite_stock_price.")
            return self.response_text(0, "價格設定完成")
        except:
            self.close()
            # print("error in add_favorite_stock_price.")
            message="500 internal database error."
            return self.response_text(1, message)
            
    def get_all_favorite_stock(self):
        try:
            query_get_favorite="SELECT*FROM favorite"
            self.connection()
            self.cur.execute(query_get_favorite)
            favorite=self.cur.fetchall()
            self.close()
            # print("Success in get_favorite_stock.")
            return favorite          
        except:
            self.close()
            # print("error in get_favorite_stock.")
            message="500 internal database error."
            return self.response_text(1, message)

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
    
    def escape_column_name(self, name): # 去除字串的''
        # This is meant to mostly do the same thing as the _process_params method
        # of mysql.connector.MySQLCursor, but instead of the final quoting step,
        # we escape any previously existing backticks and quote with backticks.
        converter = mysql.connector.conversion.MySQLConverter()
        return "`" + converter.escape(converter.to_mysql(name)).decode().replace('`', '``') + "`"

