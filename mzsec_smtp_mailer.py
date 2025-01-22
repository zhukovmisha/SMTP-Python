import email, smtplib, ssl, os, logging

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class MzSmtpEmailer:
    def __init__(
        self: str,
        subject: str,
        body: str,
        sender_email: str,
        receiver_email: str,
        password: str,
        filename: str,
    ) -> None:
        self.subject = subject
        self.body = body
        self.sender_email = sender_email
        self.receiver_email = receiver_email
        self.password = password
        self.filename = filename
        self.logger = logging.getLogger('MzSmtpEmailer.' + __name__)
    def send_mail(self, message: str) -> None:
        message = MIMEMultipart()
        self.message = message
        print(f"Sending mail to {self.receiver_email=}")
        message["From"] = self.sender_email
        message["To"] = self.receiver_email
        message["Subject"] = self.subject
        message["Bcc"] = self.receiver_email  # Recommended for mass emails
        # # Add body to email
        message.attach(MIMEText(self.body, "plain"))
        try:
            # Open PDF file in binary mode
            with open(self.filename, "rb") as attachment:
            # Add file as application/octet-stream
            # Email client can usually download this automatically as attachment
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())

            # Encode file in ASCII characters to send by email    
            encoders.encode_base64(part)

            # Add header as key/value pair to attachment part
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {self.filename}",
                )
            # Add attachment to message and convert message to string
            message.attach(part)
            text = message.as_string()
            # Log in to server using secure context and send email
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.yandex.ru", 465, context=context) as server:
                server.login(self.sender_email, self.password)
                server.sendmail(self.sender_email, self.receiver_email, text)
        except:
            self.logger.error("unable to send email",exc_info=True)

        return None