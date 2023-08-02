from rest_framework import serializers
from .models import  *

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
