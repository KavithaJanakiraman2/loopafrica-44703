from rest_framework import authentication, permissions
from rest_framework import viewsets
#from .models import OneSignalApp
from .serializers import NotificationSerializer
#from .serializers import OneSignalAppSerializer, NotificationSerializer
from .client import Client
from rest_framework.response import Response
import requests
import json

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