from rest_framework import serializers
from .models import Vendors, PurchaseOrders
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email']
        extra_kwargs = {'password': {'write_only': True}}
        
    def validate_password(self, str) -> str:
        """ A function to save the password for storing the values """
        return make_password(str)


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=255)
    class Meta:
        model = User
        fields = '__all__'


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendors
        fields= '__all__'

class PurchaseOrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model= PurchaseOrders
        fields = '__all__'

class PerformaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendors
        fields= ['on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate']
        read_only_fields= ['on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate']