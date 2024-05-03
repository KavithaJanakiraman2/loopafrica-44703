from django.urls import path, include
from rest_framework.routers import DefaultRouter

from meeting.zoom.viewsets import ZoomMeetingViewSet

router = DefaultRouter()
router.register(r'zoom-meeting', ZoomMeetingViewSet, basename='zoom-meeting')

urlpatterns = [
    path("", include(router.urls)),
]
