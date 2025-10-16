from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NotificationListView, UserDeviceViewSet

router = DefaultRouter()
router.register(r"devices", UserDeviceViewSet, basename="devices")

urlpatterns = [
    path("", NotificationListView.as_view(), name="notification-list"),
    path("", include(router.urls)),
]
