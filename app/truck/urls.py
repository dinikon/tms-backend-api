# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import CalculateDistanceAPIView

router = DefaultRouter()



urlpatterns = [
    path('truck/truck-nearby/', CalculateDistanceAPIView.as_view(), name='truck-nearby'),
]
