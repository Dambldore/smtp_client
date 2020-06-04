import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import sys

smtp_host = "smtp.yandex.ru"
login = ""
password = ""
recipients_emails = []
attachment_names = []

with open("plain.txt", "r", encoding="utf-8") as f:
    text = f.read()

with open("config.txt", "r", encoding="utf-8") as f:
    recipients_emails = list(f.readline().split(","))
    for i in range(len(recipients_emails)):
        recipients_emails[i] = recipients_emails[i].replace("\n", "")
        recipients_emails[i] = recipients_emails[i].replace(" ", "")
    mail_header = f.readline()
    attachment_names = list(f.readline().split(","))
    for i in range(len(attachment_names)):
        attachment_names[i] = attachment_names[i].replace("\n", "")
        attachment_names[i] = attachment_names[i].replace(" ", "")


msg = MIMEMultipart()
part = MIMEText(text, "plain", "utf-8")
msg.attach(part)

for i in range(len(attachment_names)):
    part = MIMEApplication(open(attachment_names[i], "rb").read())
    part.add_header("Content-Disposition", "attachment", filename=attachment_names[i])
    msg.attach(part)

msg["Subject"] = Header(mail_header, "utf-8")
msg["From"] = login
msg["To"] = ",".join(recipients_emails)

s = smtplib.SMTP(smtp_host, 587, timeout=10)
try:
    s.starttls()
    s.login(login, password)
    s.sendmail(msg['From'], recipients_emails, msg.as_string())
finally:
    s.quit()
