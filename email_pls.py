# import smtplib, ssl
#
# smtp_server = "smtp-relay.brevo.com"
# port = 587  # For starttls
# sender_email = "hardtofindaname23@gmail.com"
# password = "24jS5mkvYL9HqFnz"
#
# # Create a secure SSL context
# context = ssl.create_default_context()
#
# # Try to log in to server and send email
# try:
#     server = smtplib.SMTP(smtp_server,port)
#     # server.ehlo() # Can be omitted
#     server.starttls(context=context) # Secure the connection
#     # server.ehlo() # Can be omitted
#     server.login(sender_email, password)
#     # TODO: Send email here
#     server.sendmail(sender_email, "paul.orasan@gmail.com", "A MERS")
# except Exception as e:
#     # Print any error messages to stdout
#     print(e)
# finally:
#     server.quit()
from email_service import EmailService

email_service = EmailService("picamrr@gmail.com", "qrkoubzjvmfulsfc")
email_service.send_notification_access_granted("paul.orasan@gmail.com")