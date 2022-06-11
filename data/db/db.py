import mysql.connector
from dotenv import load_dotenv, dotenv_values

env='.env' # 執行環境
load_dotenv(override=True)

mydb=mysql.connector.connect(
    # host="localhost",
    # user="root",
    # password=dotenv_values(env)['mysql_password'],
    # port=dotenv_values(env)['mysql_port2'],
    host=dotenv_values(env)["RDS_host"],
    user=dotenv_values(env)["user"],
    password=dotenv_values(env)['password'],
    database="stock_project",
    auth_plugin="mysql_native_password",
    port=dotenv_values(env)['port'],
)

mycursor=mydb.cursor()

# mycursor.execute("SHOW DATABASES")
# for db in mycursor:
#     print(db)

# mycursor.execute("CREATE DATABASE stock_project")
# mycursor.execute("DROP TABLE stock_history")
# mycursor.execute("DROP TABLE favorite")
# mycursor.execute("DROP TABLE stock_eps_roe")
# mycursor.execute("DROP TABLE stock")

# mycursor.execute("DROP TABLE member")


# ---stock table---
# mycursor.execute("CREATE TABLE stock (stock_id VARCHAR(256) PRIMARY KEY NOT NULL, stock_name VARCHAR(255) NOT NULL)")
# mycursor.execute("ALTER TABLE stock ADD time DATETIME NOT NULL DEFAULT NOW()")

# ---stock_history table---
# mycursor.execute("CREATE TABLE stock_history (id BIGINT PRIMARY KEY NOT NULL AUTO_INCREMENT, stock_id VARCHAR(256) NOT NULL)")
# mycursor.execute("ALTER TABLE stock_history ADD open INT NOT NULL")
# mycursor.execute("ALTER TABLE stock_history ADD low INT NOT NULL")
# mycursor.execute("ALTER TABLE stock_history ADD high INT NOT NULL")
# mycursor.execute("ALTER TABLE stock_history ADD close INT NOT NULL")
# mycursor.execute("ALTER TABLE stock_history ADD volume INT NOT NULL")
# mycursor.execute("ALTER TABLE stock_history ADD PER INT NOT NULL")
# mycursor.execute("ALTER TABLE stock_history ADD dividend_yield INT NOT NULL")
# mycursor.execute("ALTER TABLE stock_history ADD PBR INT NOT NULL")
# mycursor.execute("ALTER TABLE stock_history ADD EPS INT NOT NULL")
# mycursor.execute("ALTER TABLE stock_history ADD time VARCHAR(255) NOT NULL")
# mycursor.execute("ALTER TABLE stock_history ADD FOREIGN KEY (stock_id) REFERENCES stock(stock_id)")

# mycursor.execute("ALTER TABLE stock_history MODIFY PER INT NOT NULL DEFAULT 0")
# mycursor.execute("ALTER TABLE stock_history MODIFY dividend_yield INT NOT NULL DEFAULT 0")
# mycursor.execute("ALTER TABLE stock_history MODIFY PBR INT NOT NULL DEFAULT 0")
# mycursor.execute("ALTER TABLE stock_history MODIFY EPS INT NOT NULL DEFAULT 0")



# mycursor.execute("ALTER TABLE stock_history DROP COLUMN EPS")


# ---stock_eps_roe table---
# mycursor.execute("CREATE TABLE stock_eps_roe (id BIGINT PRIMARY KEY NOT NULL AUTO_INCREMENT, stock_id VARCHAR(256) NOT NULL)")
# mycursor.execute("ALTER TABLE stock_eps_roe ADD year VARCHAR(255) NOT NULL")
# mycursor.execute("ALTER TABLE stock_eps_roe ADD ROE VARCHAR(255) NOT NULL")
# mycursor.execute("ALTER TABLE stock_eps_roe ADD ROA VARCHAR(255) NOT NULL")
# mycursor.execute("ALTER TABLE stock_eps_roe ADD EPS VARCHAR(255) NOT NULL")
# mycursor.execute("ALTER TABLE stock_eps_roe ADD BPS VARCHAR(255) NOT NULL")
# mycursor.execute("ALTER TABLE stock_eps_roe ADD time DATETIME NOT NULL DEFAULT NOW()")
# mycursor.execute("ALTER TABLE stock_eps_roe ADD FOREIGN KEY (stock_id) REFERENCES stock(stock_id)")

# mycursor.execute("ALTER TABLE stock_info DROP COLUMN year")

# mycursor.execute("DESCRIBE stock_info") # 各column的屬性
# result=mycursor.fetchall()
# print(result)

# mycursor.execute("SELECT*FROM stock_info") # 各column的屬性
# result=mycursor.fetchall()
# print(result)


# ---member table---
# mycursor.execute("CREATE TABLE member (id BIGINT PRIMARY KEY NOT NULL AUTO_INCREMENT, username VARCHAR(255) NOT NULL)")
# mycursor.execute("ALTER TABLE member ADD email VARCHAR(255) NOT NULL")
# mycursor.execute("ALTER TABLE member ADD password VARCHAR(255) NOT NULL")
# mycursor.execute("ALTER TABLE member ADD photo VARCHAR(255)")
# mycursor.execute("ALTER TABLE member ADD creation_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP")
# mycursor.execute("ALTER TABLE member ADD email_status INT")
# mycursor.execute("ALTER TABLE member ADD push_token VARCHAR(65000)")

# mycursor.execute("ALTER TABLE member DROP push_token")

# mycursor.execute("DESCRIBE member") # 各column的屬性
# result=mycursor.fetchall()
# print(result)

# ---favorite table---
# mycursor.execute("CREATE TABLE favorite (id BIGINT PRIMARY KEY NOT NULL AUTO_INCREMENT, user_id BIGINT NOT NULL)")
# mycursor.execute("ALTER TABLE favorite ADD stock_id VARCHAR(256) NOT NULL")
# mycursor.execute("ALTER TABLE favorite ADD price BIGINT")
# mycursor.execute("ALTER TABLE favorite ADD creation_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP")
# mycursor.execute("ALTER TABLE favorite ADD FOREIGN KEY (user_id) REFERENCES member(id)")
# mycursor.execute("ALTER TABLE favorite ADD FOREIGN KEY (stock_id) REFERENCES stock(stock_id)")


# mycursor.execute("DESCRIBE favorite") # 各column的屬性
# result=mycursor.fetchall()
# print(result)

# ---message_board table---
# mycursor.execute("CREATE TABLE message_board (id BIGINT PRIMARY KEY NOT NULL AUTO_INCREMENT, user_id BIGINT NOT NULL)")
# mycursor.execute("ALTER TABLE message_board ADD stock_id VARCHAR(255) NOT NULL")
# mycursor.execute("ALTER TABLE message_board ADD message VARCHAR(255) NOT NULL")
# mycursor.execute("ALTER TABLE message_board ADD FOREIGN KEY (stock_id) REFERENCES stock(stock_id)")
# mycursor.execute("ALTER TABLE message_board ADD FOREIGN KEY (user_id) REFERENCES member(id)")
# mycursor.execute("ALTER TABLE message_board ADD creation_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP")
