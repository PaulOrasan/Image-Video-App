import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

GRANTED_MESSAGE = "You have been granted access to the demo"
REVOKED_MESSAGE = "You have been revoked access to the demo"

class EmailService:
    def __init__(self, sender_email, sender_pass):
        self.sender_email = sender_email
        self.sender_pass = sender_pass

    def send_notification_access_granted(self, recipient_email):
        return self._send_notification_to_user(recipient_email, GRANTED_MESSAGE)

    def send_notification_access_revoked(self, recipient_email):
        return self._send_notification_to_user(recipient_email, REVOKED_MESSAGE)

    def _send_notification_to_user(self, recipient_email, message):
        msg = MIMEMultipart()
        msg['From'] = self.sender_email
        msg['To'] = recipient_email
        msg['Subject'] = 'Authorization Status'

        # Attach the message to the MIME structure
        msg.attach(MIMEText(message, 'plain'))

        try:
            # Connect to the SMTP server
            smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
            smtp_server.starttls()

            # Log in to the sender's email account
            smtp_server.login(self.sender_email, self.sender_pass)

            # Send the email
            smtp_server.sendmail(self.sender_email, recipient_email, msg.as_string())
            smtp_server.quit()
            return True
        except smtplib.SMTPException:
            return False