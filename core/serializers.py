from rest_framework import serializers
from .models import Owner,Store
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed

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

class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = Owner
        field = ['token']


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)
    username = serializers.CharField(
        max_length=255, min_length=3, read_only=True)

    tokens = serializers.SerializerMethodField()

    class Meta:
        model = Owner
        fields = ['email', 'password', 'username', 'tokens']

    def get_tokens(self, obj):
        user = Owner.objects.get(email=obj['email'])

        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']
        }

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')

        user = auth.authenticate(email=email, password=password)

        if not user:
            raise AuthenticationFailed('Invalid credentials, try again.')

        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin.')

        if not user.is_verified:
            raise AuthenticationFailed('Email is not verified.')

        return {
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens
        }
