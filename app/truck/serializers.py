# serializers.py
from rest_framework import serializers
from .models import CRMTrucks, PostalCodeInfo


class CRMTrucksSerializer(serializers.ModelSerializer):
    class Meta:
        model = CRMTrucks
        fields = '__all__'


class CRMPostalCodeInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostalCodeInfo
        fields = '__all__'
