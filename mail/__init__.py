import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from .config import config

class Mail:
    def __init__(self):
        self.params = config(filename='credentials.ini', section='mail_cred')
        self.port = 465
        self.smtp_server_domain_name = "smtp.gmail.com"
        self.sender_mail = self.params['sender_mail']
        self.password = self.params['password']
    
    def send(self, emails, message):
        html = f"""<html>
                    <body>
                        {''.join(message)}
                    </body>
                </html>"""
        body = MIMEText(html, 'html')
        body["Subject"] = "Boundary Reached"

        ssl_context = ssl.create_default_context()
        service = smtplib.SMTP_SSL(self.smtp_server_domain_name, self.port, context=ssl_context)
        service.login(self.sender_mail, self.password)
        
        for email in emails:
            result = service.sendmail(self.sender_mail, email, body.as_string())

        service.quit()
