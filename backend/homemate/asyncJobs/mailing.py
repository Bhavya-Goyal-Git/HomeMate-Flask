from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from homemate import app
from jinja2 import Template
import os

def send_email(to_address,subject,message):
    msg = MIMEMultipart()
    msg["From"] = app.config["SENDER_ADDRESS"]
    msg["To"] = to_address
    msg["Subject"] = subject
    msg.attach(MIMEText(message,"html"))
    try:
        s= smtplib.SMTP(host=app.config["SMTP_SERVER_HOST"],port=app.config["SMTP_SERVER_PORT"])
        s.login(app.config["SENDER_ADDRESS"],app.config["SENDER_PASSWORD"])
        s.send_message(msg)
        s.quit()
        return True
    except:
        return False

def format_message(template_file,data=None):
    if data is None:
        data = {}
    path = os.path.join(app.root_path,"mail_templates",template_file)
    with open(path) as _file:
        template = Template(_file.read())
        return template.render(data=data)