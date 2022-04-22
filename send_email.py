from email.mime.multipart import MIMEMultipart
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import flash


def send_email(To, Token):
    # create message object instance
    msg = MIMEMultipart()

    message = "Hi, Your Account has been Registered Successfully! " \
              "\n Please Click the below link to activate your account  \n http://127.0.0.1:4040/activation?activate=" \
              + Token

    # setup the parameters of the message
    password = "Test@12345"
    msg['From'] = "valarmathyb123@gmail.com"
    msg['To'] = To
    msg['Subject'] = "Account Activation"

    # add in the message body
    msg.attach(MIMEText(message, 'plain'))

    # create server
    server = smtplib.SMTP('smtp.gmail.com: 587')

    server.starttls()

    # Login Credentials for sending the mail
    server.login(msg['From'], password)

    # send the message via the server.
    server.sendmail(msg['From'], msg['To'], msg.as_string())

    server.quit()

    print("successfully sent email to %s:" % (msg['To']))




