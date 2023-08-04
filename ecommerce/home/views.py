from django.shortcuts import render
import uuid
from .serilalizer import *
from .models import *
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAuthenticatedOrReadOnly
from rest_framework import viewsets


class ItemViewset(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def create(self,request,*args,**kwargs):
        try:
            data = request.data
            user = request.user
            item.objects.create(user = user,product_image = data.get('product_image'),
                                        title = data.get('title'),price = data.get('price'),
                                        catagory = data.get('catagory'),lable = data.get('lable'),
                                        discount_price = data.get('discount_price'),description = data.get('description'))

            return Response({'data':{'msg':'item created'}},status=HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({'msg':'something went wrong '},status=HTTP_400_BAD_REQUEST)


class ItemsListViewset(viewsets.ViewSet):

    def list(self,request,*args,**kwargs):
        try:
            object = item.objects.all()
            sr = ItemSerializer(object,many=True).data
            return Response(sr)
        except Exception as e:
            print(e)

class OrderItemsViewset(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def create(self,request,*args,**kwargs):
        try:
            data = request.data
            orderitem.objects.create(user = request.user,
                                     items = item.objects.get(uuid = data.get('items')),
                                     quntity = data.get('quntity'))
            return Response({'data':{'msg':'order created'}},status=HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({'data':{'msg':'something went wrong'}},status=HTTP_400_BAD_REQUEST)
