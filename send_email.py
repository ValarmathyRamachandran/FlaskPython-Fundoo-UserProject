import smtplib

conn = smtplib.SMTP('imap.gmail.com', 587)
conn.ehlo()
conn.starttls()
conn.login('valarmathyb123@gmail.com', 'Test@12345')

conn.sendmail('valarmathyb123@gmail.com', 'valarmathyb123@gmail.com',
              'Hi Please click the below link to activate your account')
conn.quit()
