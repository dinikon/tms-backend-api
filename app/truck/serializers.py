from rest_framework import serializers
from .models import (
    PostalCodeInfo, CRMCrossBorder, CRMCertificate, CRMPreferredLoad, CRMTrucks,
    CRMDimensions, CRMTruckNotes, CRMTruckLocations
)

class PostalCodeInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostalCodeInfo
        fields = '__all__'

class CRMCrossBorderSerializer(serializers.ModelSerializer):
    class Meta:
        model = CRMCrossBorder
        fields = '__all__'

class CRMCertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CRMCertificate
        fields = '__all__'

class CRMPreferredLoadSerializer(serializers.ModelSerializer):
    class Meta:
        model = CRMPreferredLoad
        fields = '__all__'

class CRMDimensionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CRMDimensions
        fields = '__all__'

class CRMTruckNotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CRMTruckNotes
        fields = '__all__'

class CRMTruckLocationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CRMTruckLocations
        fields = '__all__'

class CRMTrucksSerializer(serializers.ModelSerializer):
    dimensions = CRMDimensionsSerializer()
    notes = CRMTruckNotesSerializer(source='crmtrucknotes_set', many=True)
    locations = CRMTruckLocationsSerializer(source='crmtrucklocations_set', many=True)
    cross_borders = CRMCrossBorderSerializer(many=True)
    certificates = CRMCertificateSerializer(many=True)
    preferred_loads = CRMPreferredLoadSerializer(many=True)

    class Meta:
        model = CRMTrucks
        fields = '__all__'
