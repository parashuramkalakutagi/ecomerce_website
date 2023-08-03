from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import *
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid


class Login(models.Model):
    phone_number = models.CharField(max_length=13,unique=True)
    otp = models.CharField(max_length=6)
    is_verified = models.BooleanField(default=False)


    def __str__(self):
        return self.phone_number


class User(AbstractUser):
    email = models.EmailField(unique=True,null=True,blank=True)
    phone_number = models.CharField(max_length=12,null=True,blank=True)
    password = models.CharField(max_length=10)
    confirm_password = models.CharField(max_length=10)
    otp = models.CharField(max_length=6,null=True,blank=True)
    otp_1 = models.CharField(max_length=6,null=True,blank=True)
    username = models.CharField(max_length=100)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()
    def __str__(self):
        return self.email