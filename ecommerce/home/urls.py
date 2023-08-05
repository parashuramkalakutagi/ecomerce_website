
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from home.views import *

router = DefaultRouter()

router.register('ItemViewset',ItemViewset,basename='ItemViewset')
router.register('ItemsListViewset',ItemsListViewset,basename='ItemsListViewset')
router.register('OrderItemsViewset',OrderItemsViewset,basename='OrderItemsViewset')
router.register('OrderItemsList',OrderItemsList,basename='OrderItemsList')
router.register('OrderViewset',OrderViewset,basename='OrderViewset')
router.register('orderList',orderList,basename='orderList')
router.register('ordercountViewset',ordercountViewset,basename='ordercountViewset')




urlpatterns = [
    path('',include(router.urls)),
]
