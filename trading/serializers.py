# trading/serializers.py

from rest_framework import serializers
from .models import  Strategy, Trade
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name']
        extra_kwargs = {
            'password': {'write_only': True},  # Ensure password is write-only
        }

    def create(self, validated_data):
        # Create a new user and ensure the password is hashed
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],  # Automatically hashes password
            email=validated_data.get('email', ''),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user

    def update(self, instance, validated_data):
        # Update the user, hashing password if it's in the validated data
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)

        # Hash password if provided
        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)
        instance.save()
        return instance




# Serializer for the Strategy model
class StrategySerializer(serializers.ModelSerializer):
    class Meta:
        model = Strategy
        fields = ['id', 'name', 'short_window', 'long_window', 'user', 'created_at']
        read_only_fields = ['user', 'created_at']  # Ensure user and created_at are read-only

    def create(self, validated_data):
        # You can add any custom logic here if needed when creating a strategy
        return Strategy.objects.create(**validated_data)


# Serializer for the Trade model
class TradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        fields = ['id', 'strategy', 'symbol', 'price', 'quantity', 'trade_type', 'executed_at']
        read_only_fields = ['executed_at']  # You can make executed_at read-only if it's auto-generated

    def create(self, validated_data):
        # Custom logic for creating a trade (if needed)
        return Trade.objects.create(**validated_data)
