from flask import *
from dotenv import load_dotenv, dotenv_values
from api.api_stock import app_stock
from api.api_member import app_member
from api.api_email import app_email
from flask_apscheduler import APScheduler
from data.stock_price_notification import send_notification, test


# from flask_cors import CORS

env=str('.env.'+dotenv_values('.env')["MODE"])
load_dotenv(override=True)

app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
# CORS(app)

scheduler=APScheduler()

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

app.register_blueprint(app_stock, url_prefix="/api")
app.register_blueprint(app_member, url_prefix="/api")
app.register_blueprint(app_email, url_prefix="/api")

# scheduler.add_job(id="test", func=send_notification, trigger='interval', seconds=8)
scheduler.add_job(id="test", func=send_notification, trigger='cron', day_of_week='mon-fri', hour='9-14', minute='0-59')
scheduler.start()

app.debug=True
app.run(host=dotenv_values(env)["app_host"], port=5000)