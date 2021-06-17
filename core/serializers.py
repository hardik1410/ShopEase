from rest_framework import serializers
from .models import Owner,Store

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=25, min_length=8, write_only=True)

    class Meta:
        model = Owner
        fields = ['email', 'username', 'password']

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')

        if not username.isalnum():
            raise serializers.ValidationError(
                'The username should contain alphanumeric characters')

        return attrs

    def create(self, validated_data):
        return Owner.objects.create_user(**validated_data)

class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = '__all__'

class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = '__all__'