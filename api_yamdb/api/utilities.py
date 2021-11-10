import random
import string

from django.core.mail import send_mail


def get_confirmation_code():
    return ''.join(random.choices(
        string.ascii_lowercase + string.ascii_uppercase + string.digits,
        k=10))

def send_confirmation_code_email(email, confirmation_code):
    send_mail(
        subject='YaMBD confirmation code',
        message=f'Hello! Your confirmation code is {confirmation_code}.',
        from_email='register@fakeyamdb.com',
        recepient_list=[email],
        fail_silent=False
    )