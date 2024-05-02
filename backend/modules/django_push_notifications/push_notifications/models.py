from typing import Iterable
from django.db import models
from django.conf import settings
from users.models import Appointment
import os


class OneSignalApp(models.Model):
    name = models.CharField(max_length=100, null=True)
    app_id = models.CharField(max_length=255, null=True)
    api_key = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    notification_id = models.CharField(max_length=155, blank=True, null=True) # id of the notification
    Notification_type = models.CharField(max_length=155) # type of notification (android or ios push)
    title = models.CharField(max_length=155, default=None, null=True) # heading of the notification
    is_read = models.BooleanField(default=False) # whether the notification has been read by the user
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    app_id = models.CharField(max_length=255, blank=True, null=True)  # Change this to CharField to store the app_id as a string
    api_key = models.CharField(max_length=255, blank=True, null=True)  # Change this to CharField to store the API key as a string
    
    def save(self, *args, **kwargs):
        if self.app_id is None:
            one_signal_app = OneSignalApp.objects.create(
                name="OneSignalApp",  # Provide default name or modify as needed
                app_id=os.environ.get('APP_ID'),
                api_key=os.environ.get('REST_API_KEY')
            )
            self.app_id = one_signal_app.app_id  # Assign the OneSignalApp instance to app_id
            self.api_key = one_signal_app.api_key  # Assign the api_key attribute of the OneSignalApp instance
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.message}"