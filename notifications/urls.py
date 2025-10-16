from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserDeviceViewSet  # only import what exists

router = DefaultRouter()
router.register(r"devices", UserDeviceViewSet, basename="devices")

urlpatterns = [
    path("", include(router.urls)),  # only include your device routes
]
