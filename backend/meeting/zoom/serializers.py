
from rest_framework import serializers, viewsets

class ZoomMeetingSerializer(serializers.Serializer):
    class Meta:
        fields = ['id', 'type', 'topic', 'start_time']
    


