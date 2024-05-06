from rest_framework import serializers
#from .models import OneSignalApp
from .models import Notification

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

class UserNotificationSerializer(serializers.ModelSerializer):
    appointment_date = serializers.SerializerMethodField()
    consult_time = serializers.SerializerMethodField()
    doctor_name = serializers.SerializerMethodField()
    class Meta:
        model = Notification
        fields = ['id','message','type','is_read','created_at', 'title', 'appointment_date', 'consult_time', 'doctor_name']
    
    def get_appointment_date(self, obj):
        return obj.appointment.date.strftime("%Y-%m-%d") if obj.appointment else None

    def get_consult_time(self, obj):
        return obj.appointment.consult_time.strftime("%H:%M:%S") if obj.appointment else None

    def get_doctor_name(self, obj):
        return obj.appointment.doctor.user.get_full_name() if obj.appointment else None