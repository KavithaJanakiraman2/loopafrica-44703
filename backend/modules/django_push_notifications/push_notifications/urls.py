from django.urls import path, include
from rest_framework.routers import DefaultRouter
#from .viewsets import OneSignalAppViewSet
from .viewsets import NotificationViewSet, NotificationDetailsBySubscriptionViewSet, UserNotificationViewset


router = DefaultRouter()
# because we are using a custom queryset for our viewset, the basename
# must be specified explicitly here. See: https://www.django-rest-framework.org/api-guide/routers/#Usage
# Your policy will be available at : /modules/privacy-policy/
#router.register("", OneSignalAppViewSet, basename="onesignalapp")
router.register(r'notifications', NotificationViewSet, basename='notifications')


urlpatterns = [
    path("", include(router.urls)),
    path('notification-details/<str:subscription_id>/', NotificationDetailsBySubscriptionViewSet.as_view({'get': 'retrieve'}), name='notification-details-subscription'),
    path('user-notifications/<user_id>/', UserNotificationViewset.as_view({'get': 'list'}), name='notification-details-user'),
    # path('notifications/', NotificationViewSet.as_view({'get': 'list', 'post': 'create'}), name='notifications'),
    # path('notifications/<int:pk>/', NotificationViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'}), name='notification'),
    # path('notifications/history/', NotificationViewSet.as_view({'get': 'history'}), name='notification_history'),
]