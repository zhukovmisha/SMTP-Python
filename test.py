import os
from mzsec_smtp_mailer import MzSmtpEmailer

password = os.environ.get("APP_PASSWD")

var1 = MzSmtpEmailer(
    subject = "An email with attachment from Python",
    body = "This is an email with attachment sent from Python",
    sender_email = "mzsec@yandex.ru",
    receiver_email = "zhukovmisha@gmail.com",
    password = password,
    filename = "document.pdf",
    )

result = var1.send_mail("Hello!")

print(result)