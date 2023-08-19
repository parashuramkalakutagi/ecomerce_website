from django.shortcuts import render
import uuid
from .serilalizer import *
from .models import *
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAuthenticatedOrReadOnly
from rest_framework import viewsets
from django.db.models import Sum,Max,Min,Count
from .main import RazorpayClient

rz_clint = RazorpayClient()



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
                                        discount_price = data.get('discount_price'),description = data.get('description'),
                                currency = 'INR')



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


class OrderItemsList(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def list(self,request,*args,**kwargs):
        try:
            object = orderitem.objects.filter(user = request.user).values_list('uuid','items','quntity').distinct()[:]
            return Response(object)
        except Exception as e:
            print(e)
            return Response({'data':{'msg':'something went wrong'}},status=HTTP_400_BAD_REQUEST)


class OrderViewset(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def create(self,request,*args,**kwargs):
        try:
            data = request.data
            order.objects.create(user = request.user ,
                                 items = orderitem.objects.get(uuid = data.get('items')),
                                 ordered = 'True',amount=data.get('amount'),currency = 'INR')

            responce = rz_clint.create_order(amount=int(data.get('amount')),currency='INR')


            return  Response({'data':{'payment_responce':responce}},status=HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({'data':{'msg':'something went wrong...'}},status=HTTP_400_BAD_REQUEST)

    def delete(self,request,*args,**kwargs):
        try:
            data = request.data
            object = order.objects.get(user = request.user , uuid = data.get('uuid'))
            if not object:
                return Response({'data':{'msg':'invalid order id ...'}},status=HTTP_400_BAD_REQUEST)
            object.delete()
            return Response({'data':{'msg':'order has been canceld ...!'}},status=HTTP_200_OK)
        except Exception as e:
            print(e)



class orderList(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self,request):
        try:
            object = order.objects.filter(user = request.user).order_by('ordered_date')
            sr = orderserializer(data=object,many=True)
            if sr.is_valid():
                sr.save()
            return Response(sr.data)
        except Exception as e:
            print(e)

class ordercountViewset(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self,request,*args,**kwargs):
        try:
            object = order.objects.values('items').annotate(count = Count('items'))
            return Response(object)
        except Exception as e:
            print(e)


class TransactionViewset(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self,request,*args,**kwargs):
        try:
            data = request.data
            data['user'] = request.user
            sr = TransactionSerializer(data=data)

            if sr.is_valid():
                rz_clint.verify_payment(
                    razorpay_order_id=sr.validated_data.get('order_id'),
                    razorpay_singnature=sr.validated_data.get('signature'),
                    razorpay_payment_id=sr.validated_data.get('payment_id')
                )
                sr.save()
                responce = {
                    'status':HTTP_201_CREATED,
                    'message':'payment succesfull',
                    'data':sr.data
                }
                return Response(responce,status=HTTP_201_CREATED)

            else:
                response = {'status': HTTP_400_BAD_REQUEST,
                            'message': 'bad request',
                            'error': sr.errors}

                return Response(response, status=HTTP_400_BAD_REQUEST)

        except Exception as e:
            response = {'status': HTTP_400_BAD_REQUEST,
                        'message': 'bad request',
                        'error': e}
            return Response(response, status=HTTP_400_BAD_REQUEST)
