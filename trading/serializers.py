# trading/serializers.py

from rest_framework import serializers
from .models import  Strategy, Trade, StrategyConfiguration
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


class StrategySerializer(serializers.ModelSerializer):
    # This will allow us to pass a list of configuration parameters when creating/updating a strategy
    configurations = serializers.JSONField(write_only=True, required=False)
    template_type = serializers.CharField(write_only=True, required=False)


    class Meta:
        model = Strategy
        fields = ['id', 'name', 'description', 'status', 'is_prebuilt', 'is_customizable', 'template_type', 'user', 'created_at', 'configurations']
        read_only_fields = ['user', 'created_at']  # Ensure 'user' and 'created_at' are read-only fields

    def create(self, validated_data):
        # Extract configurations if present
        configurations = validated_data.pop('configurations', None)
        template_type = validated_data.pop('template_type', None)

        
        # Create the strategy instance
        strategy = Strategy.objects.create(user=self.context['request'].user, **validated_data)

        # If configurations were provided, save them to StrategyConfiguration
        if configurations:
            for param_name, param_value in configurations.items():
                StrategyConfiguration.objects.create(strategy=strategy, parameter_name=param_name, parameter_value=param_value)

        return strategy

    def update(self, instance, validated_data):
        # Extract configurations if present
        configurations = validated_data.pop('configurations', None)

        # Update strategy fields
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.status = validated_data.get('status', instance.status)
        instance.is_prebuilt = validated_data.get('is_prebuilt', instance.is_prebuilt)
        instance.is_customizable = validated_data.get('is_customizable', instance.is_customizable)
        instance.template_type = validated_data.get('template_type', instance.template_type)
        instance.save()

        # If configurations were provided, update the StrategyConfiguration model
        if configurations:
            # Clear existing configurations (if desired) and replace with the new ones
            StrategyConfiguration.objects.filter(strategy=instance).delete()  # Optional: remove if you want to keep existing ones
            for param_name, param_value in configurations.items():
                StrategyConfiguration.objects.create(strategy=instance, parameter_name=param_name, parameter_value=param_value)

        return instance

# Serializer for the Trade model
class TradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        fields = ['id', 'strategy', 'symbol', 'price', 'quantity', 'trade_type', 'executed_at']
        read_only_fields = ['executed_at']  # You can make executed_at read-only if it's auto-generated

    def create(self, validated_data):
        # Custom logic for creating a trade (if needed)
        return Trade.objects.create(**validated_data)
