from rest_framework import viewsets
from .models import (
    PostalCodeInfo, CRMCrossBorder, CRMCertificate, CRMPreferredLoad, CRMTrucks,
    CRMDimensions, CRMTruckNotes, CRMTruckLocations
)
from .serializers import (
    PostalCodeInfoSerializer, CRMCrossBorderSerializer, CRMCertificateSerializer, CRMPreferredLoadSerializer,
    CRMTrucksSerializer, CRMDimensionsSerializer, CRMTruckNotesSerializer, CRMTruckLocationsSerializer
)

class PostalCodeInfoViewSet(viewsets.ModelViewSet):
    queryset = PostalCodeInfo.objects.all()
    serializer_class = PostalCodeInfoSerializer

class CRMCrossBorderViewSet(viewsets.ModelViewSet):
    queryset = CRMCrossBorder.objects.all()
    serializer_class = CRMCrossBorderSerializer

class CRMCertificateViewSet(viewsets.ModelViewSet):
    queryset = CRMCertificate.objects.all()
    serializer_class = CRMCertificateSerializer

class CRMPreferredLoadViewSet(viewsets.ModelViewSet):
    queryset = CRMPreferredLoad.objects.all()
    serializer_class = CRMPreferredLoadSerializer

class CRMTrucksViewSet(viewsets.ModelViewSet):
    queryset = CRMTrucks.objects.all()
    serializer_class = CRMTrucksSerializer

class CRMDimensionsViewSet(viewsets.ModelViewSet):
    queryset = CRMDimensions.objects.all()
    serializer_class = CRMDimensionsSerializer

class CRMTruckNotesViewSet(viewsets.ModelViewSet):
    queryset = CRMTruckNotes.objects.all()
    serializer_class = CRMTruckNotesSerializer

class CRMTruckLocationsViewSet(viewsets.ModelViewSet):
    queryset = CRMTruckLocations.objects.all()
    serializer_class = CRMTruckLocationsSerializer
