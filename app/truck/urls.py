# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import CRMTrucksViewSet, CRMPostalCodeInfoViewSet

router = DefaultRouter()
router.register(r'trucks', CRMTrucksViewSet)
router.register(r'postcodeinfo', CRMPostalCodeInfoViewSet)

urlpatterns = [
    path('truck/', include(router.urls)),
]
