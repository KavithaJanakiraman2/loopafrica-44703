from rest_framework import authentication, permissions
from rest_framework import viewsets
#from .models import OneSignalApp
from .serializers import NotificationSerializer
#from .serializers import OneSignalAppSerializer, NotificationSerializer
from .client import Client
from rest_framework.response import Response
import requests
import json
from .utils import APP_ID, REST_API_KEY
from datetime import datetime
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.views import APIView
from rest_framework import status


# class OneSignalAppViewSet(viewsets.ModelViewSet):
#     queryset = OneSignalApp.objects.all()
#     serializer_class = OneSignalAppSerializer

#     def create(self, request, *args, **kwargs):
#         client = Client()
#         response = client.create_app(request.data)
#         return super().create(request, *args, **kwargs)

class NotificationViewSet(viewsets.ViewSet):
    serializer_class = NotificationSerializer

    def create(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            #client = Client(serializer.validated_data['app_id'], serializer.validated_data['rest_api_key'])
            notification_content = {
                "included_segments": serializer.validated_data['included_segments'],
                "data": serializer.validated_data['data'],
                "contents": serializer.validated_data['contents']
            }
            #client.create_notification(notification_content)
            headers = {"Content-Type": request.headers['Content-Type'], "Authorization": request.headers['Authorization'], "Accept": request.headers['Accept']}
            response = requests.post("https://onesignal.com/api/v1/notifications/", headers=headers, data=json.dumps(request.data))
            return Response({"message": "Notification created", "response": response.json()})
        except Exception as e:
            return Response({"message": "Error creating notification", "error": str(e)})

    def list(self, request):
        app_id = request.query_params.get('app_id')
        url = f'https://api.onesignal.com/notifications/?app_id={app_id}'
        headers = {
            "Authorization": request.headers['Authorization']
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return Response(response.json())
        else:
            return Response({'error': 'Could not retrieve notification'}, status=response.status_code)

    def retrieve(self, request, pk=None):
        app_id = request.query_params.get('app_id')
        url = f'https://api.onesignal.com/notifications/{pk}?app_id={app_id}'
        headers = {
            "Authorization": request.headers['Authorization']
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return Response(response.json())
        else:
            return Response({'error': 'Could not retrieve notification'}, status=response.status_code)

    def destroy(self, request, pk=None):
        app_id = request.query_params.get('app_id')
        url = f'https://api.onesignal.com/notifications/{pk}?app_id={app_id}'
        headers = {
            "Authorization": request.headers['Authorization']
        }
        response = requests.delete(url, headers=headers)
        if response.status_code == 200:
            return Response({'message': 'Notification cancelled'})
        else:
            return Response({'error': 'Could not cancel notification'}, status=response.status_code)

    def history(self, request):
        # Add your logic to retrieve and return the notification history
        pass

class NotificationDetailsBySubscriptionViewSet(viewsets.ViewSet):
    
    '''To retrieve notifications associated with the provided subscription ID and future appointment dates'''
    def retrieve(self, request, subscription_id=None):
        try:
            # Fetch notifications associated with the app ID
            headers = {
                "accept": "application/json",
                "content-type": "application/json",
                "Authorization": f"Basic {REST_API_KEY}"
            }
            url = f"https://onesignal.com/api/v1/notifications?app_id={APP_ID}"
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
            notifications_data = response.json()
            
            # Check if notifications are present in the response
            if "notifications" in notifications_data:
                notifications = notifications_data["notifications"]
                
                # Filter notifications by the provided subscription ID and future appointment dates
                filtered_notifications = []
                current_datetime = datetime.now()
                for notification in notifications:
                    include_player_ids = notification.get("include_player_ids", [])
                    send_after = notification.get("send_after")
                    appointment_date_str = notification.get("data", {}).get("appointment_date")
                    consult_time_str = notification.get("data", {}).get("consult_time")
                    if send_after and appointment_date_str and consult_time_str:
                        notification_datetime = datetime.strptime(f"{appointment_date_str} {consult_time_str}", "%Y-%m-%d %H:%M:%S")
                        if subscription_id in include_player_ids and notification_datetime >= current_datetime:
                            filtered_notifications.append(notification)
                
                # Check if there are notifications associated with the subscription ID and future dates
                if filtered_notifications:
                    # Return the list of notifications
                    return Response(filtered_notifications)
                else:
                    return Response({"error": "No notifications found for the subscription ID and future dates"}, status=404)
            else:
                return Response({"error": "No notifications found"}, status=404)
                
        except requests.exceptions.RequestException as e:
            # Handle any exceptions (e.g., network errors, invalid responses)
            return Response({"error": str(e)}, status=500)
        
    '''Retrieve notifications associated with the provided external_user ID'''

class UserNotificationViewset(viewsets.ViewSet):
    def list(self, request, user_id=None):
        try:
            # Fetch notifications associated with the app ID
            headers = {
                "accept": "application/json",
                "content-type": "application/json",
                "Authorization": f"Basic {REST_API_KEY}"
            }
            url = f"https://onesignal.com/api/v1/notifications?app_id={APP_ID}"
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
            notifications_data = response.json()
            
            # Check if notifications are present in the response
            if "notifications" in notifications_data:
                notifications = notifications_data["notifications"]
                
                # Filter notifications by the provided user ID
                filtered_notifications = []
                for notification in notifications:
                    include_external_user_ids = notification.get("include_external_user_ids")
                    if include_external_user_ids and user_id in include_external_user_ids:
                        filtered_notifications.append(notification)
                
                # Check if there are notifications associated with the user ID
                if filtered_notifications:
                    # Return the list of notifications
                    return Response(filtered_notifications)
                else:
                    return Response({"error": "No notifications found for the user ID"}, status=404)
            else:
                return Response({"error": "No notifications found"}, status=404)
                
        except requests.exceptions.RequestException as e:
            # Handle any exceptions (e.g., network errors, invalid responses)
            return Response({"error": str(e)}, status=500)
