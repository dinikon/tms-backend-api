# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import (
    PostalCodeInfoViewSet, CRMCrossBorderViewSet, CRMCertificateViewSet, CRMPreferredLoadViewSet,
    CRMTrucksViewSet, CRMDimensionsViewSet, CRMTruckNotesViewSet, CRMTruckLocationsViewSet
)

router = DefaultRouter()
router.register(r'postal-code-info', PostalCodeInfoViewSet)
router.register(r'cross-border', CRMCrossBorderViewSet)
router.register(r'certificate', CRMCertificateViewSet)
router.register(r'preferred-load', CRMPreferredLoadViewSet)
router.register(r'trucks', CRMTrucksViewSet)
router.register(r'dimensions', CRMDimensionsViewSet)
router.register(r'truck-notes', CRMTruckNotesViewSet)
router.register(r'truck-locations', CRMTruckLocationsViewSet)

urlpatterns = [
    path('truck/', include(router.urls)),
]
