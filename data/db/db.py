import mysql.connector
from dotenv import load_dotenv, dotenv_values

env='.env' # 執行環境
load_dotenv(override=True)

mydb=mysql.connector.connect(
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
# mycursor.execute("DROP TABLE stock_info")

# ---stock table---
# mycursor.execute("CREATE TABLE stock_info (id BIGINT PRIMARY KEY NOT NULL AUTO_INCREMENT, stock_name VARCHAR(255) NOT NULL)")
# mycursor.execute("ALTER TABLE stock_info ADD stock_id INT NOT NULL")
# mycursor.execute("ALTER TABLE stock_info ADD year VARCHAR(255) NOT NULL")
# mycursor.execute("ALTER TABLE stock_info ADD ROE VARCHAR(255) NOT NULL")
# mycursor.execute("ALTER TABLE stock_info ADD ROA VARCHAR(255) NOT NULL")
# mycursor.execute("ALTER TABLE stock_info ADD EPS VARCHAR(255) NOT NULL")
# mycursor.execute("ALTER TABLE stock_info ADD BPS VARCHAR(255) NOT NULL")
# mycursor.execute("ALTER TABLE stock_info ADD time DATETIME NOT NULL DEFAULT NOW()")
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

# mycursor.execute("DESCRIBE member") # 各column的屬性
# result=mycursor.fetchall()
# print(result)

# ---favorite table---
# mycursor.execute("CREATE TABLE favorite (id BIGINT PRIMARY KEY NOT NULL AUTO_INCREMENT, user_id BIGINT NOT NULL)")
# mycursor.execute("ALTER TABLE favorite ADD stock_id INT NOT NULL")
# mycursor.execute("ALTER TABLE favorite ADD price BIGINT")
# mycursor.execute("ALTER TABLE favorite ADD creation_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP")

# mycursor.execute("ALTER TABLE favorite ADD FOREIGN KEY (user_id) REFERENCES member(id)")

# mycursor.execute("DESCRIBE favorite") # 各column的屬性
# result=mycursor.fetchall()
# print(result)