# WSGI Gunicorn
from app import app
import multiprocessing as mp

# import gevent.monkey
# gevent.monkey.patch_all() # 如 worker_class 設定為 gevent

# 一定要用 0.0.0.0，不得用 127.0.0.1
bind = "0.0.0.0:5000"
# workers = mp.cpu_count() * 2 + 1
workers = 4 # 如僅有 workers，worker_class 為 sync
threads = 4 # 每個 worker 分配的 threads 數量，如 threads > 1，worker_class 為 gthread
worker_class = "gthread"
# worker_class = "gevent" # *** 出現 error：RecursionError: maximum recursion depth exceeded，使用簡單的 web app 測試