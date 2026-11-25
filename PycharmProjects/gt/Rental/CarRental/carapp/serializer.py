from rest_framework import serializers
from .models import CarDb,RentalDb
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username','password','email']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarDb
        fields = "__all__"
        read_only_fields = ['created_at']

class RentalSerializer(serializers.ModelSerializer):
    class Meta:
        model = RentalDb
        fields = "__all__"
        read_only_fields = ['booked_at']
        read_only_fields = ['customer', 'total_amount', 'booked_at']
