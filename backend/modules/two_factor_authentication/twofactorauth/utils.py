from django.core.mail import EmailMessage
import os
 
class Util:
    @staticmethod
    def send_email(data):
        try:
            email=EmailMessage(
                subject=data['subject'],
                body=data['body'],
                from_email=os.environ.get('EMAIL_FROM'),
                to=[data['to_email']]
            )
            email.send()
            return True # return True if email is sent successfully
        except Exception as e:
            print("Error sending email:",str(e))
            return False