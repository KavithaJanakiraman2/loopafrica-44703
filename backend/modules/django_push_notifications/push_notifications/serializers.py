from rest_framework import serializers
#from .models import OneSignalApp

# class OneSignalAppSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = OneSignalApp
#         fields = '__all__'

class NotificationSerializer(serializers.Serializer):
    app_id = serializers.CharField(max_length=255)
    rest_api_key = serializers.CharField(max_length=255)
    included_aliases = serializers.ListField(child=serializers.CharField(max_length=255))
    target_channel = serializers.CharField(max_length=255)
    included_segments = serializers.ListField(child=serializers.CharField(max_length=255))
    data = serializers.DictField(child=serializers.CharField(max_length=255))
    contents = serializers.DictField(child=serializers.CharField(max_length=255))