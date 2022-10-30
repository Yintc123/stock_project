# WSGI Gunicorn
from app import app
import multiprocessing as mp

# 一定要用 0.0.0.0，不得用 127.0.0.1
bind = "0.0.0.0:5000"
# workers = mp.cpu_count() * 2 + 1
workers = 4
threads = 4