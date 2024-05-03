import requests
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateAPIView, CreateAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status, filters
from rest_framework.mixins import UpdateModelMixin
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from meeting.zoom.utils import create_meeting, generate_token
from users.models import User
from rest_framework.decorators import action
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend
from datetime import datetime
from django.db.models import Case, When, Value, IntegerField

#from meeting.zoom.models import Meeting
from meeting.zoom.serializers import ZoomMeetingSerializer

class ZoomMeetingViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ZoomMeetingSerializer

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Initialize token
        self.token = generate_token()

    def create(self, request, *args, **kwargs):
        # Call generate_token to get the access token
        if isinstance(self.token, Exception):
            return Response({"error": "Failed to generate token"}, status=500)        
        
        resp = create_meeting(request.data['topic'], request.data['type'], request.data['start_time'], self.request.user)

        return Response({"message": "Meeting created successfully", "data":resp.json()}, status=201 ) 
    
 