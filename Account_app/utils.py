''' ЗДЕСЬ Я МОГУ ОПРЕДЕЛЯТЬ ЗАДАЧИ, '''
'''Определим метод, для отправки электронных писем'''
from django.core.mail import EmailMessage
class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'], body=data['email_body'], to=[data['to_email']])
        email.send()

