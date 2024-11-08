from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

admin_email = settings.EMAIL_HOST_USER

@shared_task
def send_email_task(email_id):
    send_mail(
        'Exciting offer for you!',
        "You have got an exciting offer. Please check it out by contacting us.",
        admin_email,
        [email_id],
    )
