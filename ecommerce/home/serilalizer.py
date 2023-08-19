from rest_framework import serializers
from .models import *

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = item
        exclude = ['created_at','updated_at']

class orderserializer(serializers.ModelSerializer):
    class Meta:
        model = order
        fields = '__all__'


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Amount_transaction
        fields = '__all__'