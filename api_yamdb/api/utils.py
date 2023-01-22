from django.core.mail import send_mail
from django.conf import settings


def send_reg_mail(email, confirmation_code):
    send_mail(
        subject='Код подтверждения для получения токена.',
        message=f'Ваш код: {confirmation_code}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
    )
