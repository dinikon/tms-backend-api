from rest_framework.decorators import permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import CRMTrucks
from .serializers import CRMTrucksSerializer
from geopy.geocoders import Nominatim
from geopy.distance import geodesic


@permission_classes((permissions.AllowAny,))
class CalculateDistanceAPIView(APIView):
    def post(self, request, *args, **kwargs):
        radius = request.data.get('radius')
        address = request.data.get('address')

        if not radius or not address:
            return Response({"error": "Both 'radius' and 'address' are required."}, status=status.HTTP_400_BAD_REQUEST)

        geolocator = Nominatim(user_agent="your_app_name")
        location_title = geolocator.geocode(address)

        if not location_title:
            return Response({"error": f"Could not geocode address with title: {address}"}, status=status.HTTP_400_BAD_REQUEST)

        trucks = CRMTrucks.objects.all()
        results = []

        for truck in trucks:
            last_location = truck.crmtrucklocations_set.order_by('-created_at').first()
            if last_location:
                location_truck = geolocator.geocode(last_location.address)
                if location_truck:
                    distance = geodesic((location_title.latitude, location_title.longitude), (location_truck.latitude, location_truck.longitude)).km
                    if distance <= float(radius):
                        serializer = CRMTrucksSerializer(truck, context={'distance': distance})
                        results.append(serializer.data)

        return Response(results, status=status.HTTP_200_OK)
