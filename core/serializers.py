from django.db.models.fields import CharField
from rest_framework import serializers
from .models import Owner, ProductImage
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=25, min_length=8, write_only=True)

    class Meta:
        model = Owner
        fields = ['email', 'firstname', 'lastname', 'username', 'password']

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')
        firstname = attrs.get('firstname', '')
        lastname = attrs.get('lastname', '')

        if not username.isalnum():
            raise serializers.ValidationError(
                'The username should contain alphanumeric characters')

        return attrs

    def create(self, validated_data):
        return Owner.objects.create_user(**validated_data)


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


class RequestPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    class Meta:
        fields = ['email']


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        min_length=8, max_length=25, write_only=True)
    token = serializers.CharField(
        min_length=1, write_only=True)
    uidb64 = serializers.CharField(
        min_length=1, write_only=True)

    class Meta:
        fields = ['password', 'token', 'uidb64']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            id = force_str(urlsafe_base64_decode(uidb64))
            user = Owner.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid', 401)

            user.set_password(password)
            user.save()

            return (user)
        except Exception as e:
            raise AuthenticationFailed('The reset link is invalid', 401)
        return super().validate(attrs)


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_message = {
        'bad_token': ('Token is expired or invalid')
    }
    
    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()

        except TokenError:
            self.fail('bad_token')

class MyFileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ProductImage
        fields = ['imagePath', 'productId']

class ImageDownloadSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        fields = ['imagePath',]
