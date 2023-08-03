from rest_framework import serializers
from .models import  *
from rest_framework_simplejwt.tokens import RefreshToken

class RegisterSerialiser(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email','password','confirm_password']

    def validate(self, data):
        password = data['password']
        confirm_password = data['confirm_password']
        if password != confirm_password :
            raise serializers.ValidationError('password and confirmpassword are not matching...!')
        return data

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ['email','password']

    def validate(self, data):
        email = data['email']
        password = data['password']
        if not User.objects.filter(email = email,password= password).exists():
            raise serializers.ValidationError('invalid user')
        return data


    def jwt_token_for_user(self,data):

        user = User.objects.get(email = data['email'],password = data['password'])
        if not user:
            return {'msg':'user not found'}

        refresh = RefreshToken.for_user(user)

        return {
            'msg': 'login successfully',
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

