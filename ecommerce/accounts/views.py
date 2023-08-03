from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import *
from .serializers import *
from rest_framework_simplejwt.tokens import RefreshToken
from .helpers import send_otp_phone


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class Sent_otp(viewsets.ViewSet):

    def create(self,request,*args,**kwargs):
        try:
            data = request.data
            user = Login.objects.create(phone_number = data.get('phone_number'),otp = send_otp_phone(data.get('phone_number')))
            user.save()
            return Response({'msg':'otp sent on mobile number'},status=HTTP_201_CREATED)
        except Exception as e:
            print(e)

class VerifyOtp(viewsets.ViewSet):
    def create(self,request,*args,**kwargs):
        try:
            data = request.data
            if data.get('phone_number') is None:
                return Response({'msg':'phone number is requered'},status=HTTP_400_BAD_REQUEST)
            user = Login.objects.get(phone_number__exact = data.get('phone_number'))
            if user.otp != data.get('otp'):
                return Response({'msg':'otp dose not matched ...!'},status=HTTP_400_BAD_REQUEST)
            if user.otp == data.get('otp'):
                return Response({'data':{'msg':'otp matched..'}})
        except Exception as e:
            print(e)


class RegisteViewset(viewsets.ViewSet):
    def create(self,request,*args,**kwargs):
        try:
            data = request.data
            sr = RegisterSerialiser(data=data)
            if sr.is_valid():
                user = sr.save()
                token = get_tokens_for_user(user)
                return Response({'data':{'msg':'registration succsessfully...','token':token}},status=HTTP_201_CREATED)
            else:
                return Response(sr.errors,status=HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(e)
            return Response({'msg':'something went wrong'},status=HTTP_400_BAD_REQUEST)

class LoginViewset(viewsets.ViewSet):

    def create(self, request, *args, **kwargs):
        try:
           data = request.data
           sr = LoginSerializer(data=data)

           if not  sr.is_valid():
               return Response(sr.errors,status=HTTP_400_BAD_REQUEST)
           responce = sr.jwt_token_for_user(sr.data)

           return Response(responce,status=HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({'msg':'something went wrong '},status=HTTP_400_BAD_REQUEST)

class LogoutViewset(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def create(self,request,*args,**kwargs):
        try:
            data = request.data
            refresh  = data['Refreshtoken']
            token = RefreshToken(refresh)
            token.blacklist()
            if not token:
                return Response({'data':{'msg':'invalid token...!'}},status=HTTP_400_BAD_REQUEST)
            return Response({'data':{'msg':'logout successfully...'}},status=HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'msg':'something went wrong '},status=HTTP_400_BAD_REQUEST)

