import random
from django.core.mail import send_mail
from django.conf import settings
from .models import *
def send_via_mail(email):
    subject = f'INSTAGRAM FORGOT PASSWORD   '
    otp = random.randint(1000,9999)
    message = f'your email verification otp is {otp} '
    email_from = settings.EMAIL_HOST
    send_mail(subject,message,email_from,[email])
    user_obj = User.objects.get(email= email)
    user_obj.otp = otp
    user_obj.save()

