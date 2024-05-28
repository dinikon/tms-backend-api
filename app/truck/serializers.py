from rest_framework import serializers
from .models import CRMTrucks, CRMTruckLocations, PostalCodeInfo


class PostalCodeInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostalCodeInfo
        fields = '__all__'


class CRMTruckLocationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CRMTruckLocations
        fields = '__all__'


class CRMTrucksSerializer(serializers.ModelSerializer):
    last_location = serializers.SerializerMethodField()
    distance = serializers.SerializerMethodField()

    class Meta:
        model = CRMTrucks
        fields = '__all__'

    def get_last_location(self, obj):
        last_location = obj.crmtrucklocations_set.order_by('-created_at').first()
        if last_location:
            return CRMTruckLocationsSerializer(last_location).data
        return None

    def get_distance(self, obj):
        # Это поле будет заполняться в APIView
        return self.context.get('distance', None)
