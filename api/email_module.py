import smtplib
import email.message
from dotenv import load_dotenv, dotenv_values

env='.env'
load_dotenv(override=True)


class gmail_module():
    def __init__(self, member_email, subject):
        self.gmail_token=dotenv_values(env)["gmail_token"]
        self.server=None
        self.msg=email.message.EmailMessage()
        self.msg["From"]=dotenv_values(env)["gmail"]
        self.msg["To"]=member_email
        self.msg["Subject"]=subject

    def connection(self):
        self.server=smtplib.SMTP_SSL("smtp.gmail.com", 465) # 建立gmail伺服器連線
        self.server.login(dotenv_values(env)["gmail"], self.gmail_token)

    def close(self):
        self.server.close()

    def send_message(self, message):
        self.connection()
        self.msg.set_content(message)
        self.server.send_message(self.msg)
        self.close()
        return 0