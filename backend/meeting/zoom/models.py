import uuid
import os
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils import timezone
from users.models import User, Doctor, Appointment

class Zoom(models.Model):
    """
    Represents a Zoom meeting.
 
    Attributes:
        appointment (Appointment): The appointment associated with the Zoom meeting.
        meeting_id (str): The ID of the Zoom meeting.
        password (str): The password for the Zoom meeting.
        created_at (DateTime): The date and time when the Zoom meeting was created.
        updated_at (DateTime): The date and time when the Zoom meeting was last updated.
        created_by (User): The user who created the Zoom meeting.
        updated_by (User): The user who last updated the Zoom meeting.
    """
 
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='zoom_appointment', null=True, blank=True)
    meeting_id = models.CharField(max_length=255, null=True, blank=True)
    join_url = models.CharField(max_length=255, null=True, blank=True)
    password = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='zoom_created_by', null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='zoom_updated_by', null=True, blank=True)
 
    def __str__(self):
        return f"Zoom meeting for {self.appointment.user.username} with {self.appointment.doctor.user.username}"

class ZoomToken(models.Model):
    """
    Represents a Zoom token.
 
    Attributes:
        token (str): The Zoom token.
        expiry (DateTime): The date and time when the Zoom token expires.
        created_at (DateTime): The date and time when the Zoom token was created.
        updated_at (DateTime): The date and time when the Zoom token was last updated.
        created_by (User): The user who created the Zoom token.
        updated_by (User): The user who last updated the Zoom token.
    """
    account_id = models.CharField(max_length=255, null=True, blank=True)
    client_id = models.CharField(max_length=255, null=True, blank=True)
    client_secret = models.CharField(max_length=255, null=True, blank=True)
    token = models.TextField(null=True, blank=True)
    expiry = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='zoom_token_created_by', null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='zoom_token_updated_by', null=True, blank=True)
 
    def __str__(self):
        return f"Zoom token for {self.created_by.username}"
 
    def is_expired(self):
        return self.expiry < timezone.now()