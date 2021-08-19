from rest_framework import serializers
from core.models import Owner,Store

class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = ['firstname', 'lastname', 'username', 'email']

class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = '__all__'