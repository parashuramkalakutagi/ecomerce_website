
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from accounts.views import *

router = DefaultRouter()

router.register('Sent_otp',Sent_otp,basename='Sent_otp')
router.register('VerifyOtp',VerifyOtp,basename='VerifyOtp')

router.register('RegisteViewset',RegisteViewset,basename='RegisteViewset')



urlpatterns = [
    path('',include(router.urls)),
]
