# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import CalculateDistanceAPIView, PostalCodeInfoListView

router = DefaultRouter()



urlpatterns = [
    path('truck/truck-nearby/', CalculateDistanceAPIView.as_view(), name='truck-nearby'),
    path('truck/dic_postal_codes/', PostalCodeInfoListView.as_view(), name='postal_code_list'),
]
