import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from time import sleep
from turtle import delay

from celery import Celery
from dotenv import load_dotenv

load_dotenv()
# environment variable

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
PASSWORD = os.getenv("PASSWORD")

client = Celery('task', broker='redis://localhost:6379',
                backend='redis://localhost:6379')


@client.task
def send_email(To, Subject, template, token):
    delay(1)
    # create message object instance
    msg = MIMEMultipart()

    # message = message + Token

    # setup the parameters of the message
    password = PASSWORD
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = To
    msg['Subject'] = Subject

    # add in the message body
    # msg.attach(MIMEText(message, 'plain'))
    msg.attach(MIMEText(template + token, 'html'))

    # create server
    server = smtplib.SMTP('smtp.gmail.com: 587')

    server.starttls()

    # Login Credentials for sending the mail
    server.login(msg['From'], password)

    # send the message via the server.
    server.sendmail(msg['From'], msg['To'], msg.as_string())

    server.quit()

    print("successfully sent email to %s:" % (msg['To']))
