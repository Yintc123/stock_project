from mysql.connector.pooling import MySQLConnectionPool
from dotenv import load_dotenv, dotenv_values

env='.env' # 執行環境
load_dotenv(override=True)

conn_pool=MySQLConnectionPool(
    host=dotenv_values(env)["RDS_host"],
    user=dotenv_values(env)["user"],
    password=dotenv_values(env)['password'],
    database="stock_project",
    pool_name="myPool",
    pool_size=2,
    auth_plugin="mysql_native_password",
    port=dotenv_values(env)['port']
)