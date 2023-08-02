
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from accounts.views import *

router = DefaultRouter()



urlpatterns = [
    path('',include(router.urls)),
]
