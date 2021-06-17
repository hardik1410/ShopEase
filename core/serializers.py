from rest_framework import serializers
from .models import Owner

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