# kisi bhi app ke andar tasks.py file banao

from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_approval_email_task(email):
    print("enter in celery task")
    try:
        send_mail(
            'Approval Successful',
            'Congratulations! Your account has been approved.',
            'hamzasafeer243@gmail.com',
            [email],
            fail_silently=False,
        )
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")
    
