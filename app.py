from flask import *
from dotenv import load_dotenv, dotenv_values
from api.api_stock import app_stock
from api.api_member import app_member
from api.api_email import app_email
from api.api_message import app_message
from api.api_webpush import app_webpush
from data.stock_price_notification import send_notification, test
# from flask_socketio import SocketIO, emit


# from flask_cors import CORS

env=str('.env.'+dotenv_values('.env')["MODE"])
load_dotenv(override=True)

app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
# CORS(app)

# socket=SocketIO(app)

app.secret_key="This is an important key for sessionzxc" #seession

@app.route("/")
def index():
    return render_template("index.html")
@app.route("/<stock_id>")
def stock(stock_id):
    return render_template("stock.html")
@app.route("/member")
def member():
    return render_template("member.html")
@app.route('/sw.js', methods=['GET']) # 如無此route，error:A bad HTTP response code (404) was received when fetching the script.
def sw():
    return app.send_static_file('sw.js')

app.register_blueprint(app_stock, url_prefix="/api")
app.register_blueprint(app_member, url_prefix="/api")
app.register_blueprint(app_email, url_prefix="/api")
app.register_blueprint(app_message, url_prefix="/api")
app.register_blueprint(app_webpush, url_prefix="/api")


# some=["apple", "dog", "cat", "lion"]
# i=0
# @socket.on('message')
# def handlemsg(msg):
#     print(msg)
#     global i
#     if i < len(some):
#         socket.send(i)
#         i+=1

# app.debug=True
app.run(host=dotenv_values(env)["app_host"], port=5000)
# socket.run(app, host=dotenv_values(env)["app_host"], port=5000, debug=True)