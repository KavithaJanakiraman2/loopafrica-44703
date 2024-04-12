from rest_framework import authentication, permissions
from rest_framework import viewsets
#from .models import OneSignalApp
from .serializers import NotificationSerializer
#from .serializers import OneSignalAppSerializer, NotificationSerializer
from .client import Client
from rest_framework.response import Response
import requests
import json
from users.models import Appointment
from django.contrib.auth.models import AnonymousUser

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

    # def create(self, request):
    #     try:
    #         serializer = self.serializer_class(data=request.data)
    #         serializer.is_valid(raise_exception=True)
            
    #         appointment_data = {
    #             "doctor_name": None,  # Initialize to None
    #             "date": serializer.validated_data['date'],
    #             "consult_time": serializer.validated_data['consult_time']
    #         }
            
    #         # Fetch appointments from the database
    #         appointments = Appointment.objects.all()
            
    #         # Iterate over appointments to fetch doctor names
    #         for appointment in appointments:
    #             doctor_name = appointment.doctor.user.name
    #             # If doctor_name is not None, assign it to appointment_data
    #             if doctor_name:
    #                 appointment_data["doctor_name"] = doctor_name
    #                 # Construct notification message
    #                 notification_content = {
    #                     "included_segments": serializer.validated_data['included_segments'],
    #                     "data": serializer.validated_data['data'],
    #                     "contents": {
    #                         "en": f"Consultation with {appointment_data['doctor_name']} on {appointment_data['date']} at {appointment_data['consult_time']}"
    #                     }
    #                 }
    #                 # Send notification
    #                 headers = {"Content-Type": request.headers['Content-Type'], "Authorization": request.headers['Authorization'], "Accept": request.headers['Accept']}
    #                 response = requests.post("https://onesignal.com/api/v1/notifications/", headers=headers, data=json.dumps(notification_content))
            
    #         return Response({"message": "Notification created", "response": response.json()})
    #     except Exception as e:
    #         return Response({"message": "Error creating notification", "error": str(e)})

    # def list(self, request):
    #     # Logic to fetch and return appointment notifications with doctor details
    #     appointments = Appointment.objects.all()  # Example: Fetch appointments from database
    #     appointment_data = []  # Placeholder for appointment data
        
    #     for appointment in appointments:
    #         appointment_data.append({
    #             "doctor_name": appointment.doctor.user.name,
    #             "profile_picture": appointment.doctor.user.profile_picture.url if appointment.doctor.user.profile_picture else None,
    #             "date": appointment.date,
    #             "consult_time": appointment.consult_time
    #             #"specialized": appointment.doctor.specialized,
    #         })
        
    #     return Response(appointment_data)

    # def get(self, request):
    #     # Fetch notifications
    #     app_id = request.query_params.get('app_id')
    #     url = f'https://api.onesignal.com/notifications/?app_id={app_id}'
    #     headers = {"Authorization": request.headers['Authorization']}
    #     response = requests.get(url, headers=headers)
    #     if response.status_code == 200:
    #         notification_data = response.json()
    #     else:
    #         return Response({'error': 'Could not retrieve notification'}, status=response.status_code)

    #     # Fetch appointments for the current authenticated user
    #     appointments = Appointment.objects.filter(user=request.user)

    #     # Prepare appointment data
    #     appointment_data = []
    #     for appointment in appointments:
    #         appointment_data.append({
    #             "doctor_name": appointment.doctor.user.name,
    #             "profile_picture": appointment.doctor.user.profile_picture.url if appointment.doctor.user.profile_picture else None,
    #             "date": appointment.date,
    #             "consult_time": appointment.consult_time,
    #             # Add any additional appointment fields you want to include
    #         })

    #     # Combine notification data with appointment data
    #     combined_data = {
    #         "notifications": notification_data,
    #         "appointments": appointment_data
    #     }

        # return Response(combined_data)

    def get(self, request):
        # Check if the user is authenticated
        if isinstance(request.user, AnonymousUser):
            # Handle unauthenticated user (e.g., return an error response)
            return Response({'error': 'User is not authenticated'}, status=401)

        # Fetch notifications
        app_id = request.query_params.get('app_id')
        url = f'https://api.onesignal.com/notifications/?app_id={app_id}'
        headers = {"Authorization": request.headers['Authorization']}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            notification_data = response.json()
        else:
            return Response({'error': 'Could not retrieve notification'}, status=response.status_code)

        # Fetch appointments for the current authenticated user
        appointments = Appointment.objects.filter(user=request.user)

        # Prepare appointment data
        appointment_data = []
        for appointment in appointments:
            appointment_data.append({
                "doctor_name": appointment.doctor.user.name,
                "profile_picture": appointment.doctor.user.profile_picture.url if appointment.doctor.user.profile_picture else None,
                "date": appointment.date,
                "consult_time": appointment.consult_time,
                # Add any additional appointment fields you want to include
            })

        # Combine notification data with appointment data
        combined_data = {
            "notifications": notification_data,
            "appointments": appointment_data
        }

        return Response(combined_data)