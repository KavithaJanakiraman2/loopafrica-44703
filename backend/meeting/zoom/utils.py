from rest_framework.response import Response
from rest_framework import status
import requests
from meeting.zoom.models import Zoom, ZoomToken
from datetime import datetime, timedelta
import os
import base64

client_id = os.environ.get('ZOOM_CLIENT_ID')
client_secret = os.environ.get('ZOOM_CLIENT_SECRET')
account_id = os.environ.get('ZOOM_ACCOUNT_ID')

def generate_token():
    try:
        auth = f'{client_id}:{client_secret}'
        # encode the client_id and client_secret to base64
        encoded_auth = base64.b64encode(auth.encode('utf-8')).decode('utf-8')
        # Define the headers
        headers = {
                    'Authorization': f'Basic {encoded_auth}'
        }
        # Define the params to be sent to the Zoom API
        params = {
            "grant_type": "account_credentials",
            "account_id": account_id
        }
        # make the post request to create a meeting
        response = requests.post('https://zoom.us/oauth/token', headers=headers, params=params)
        # check if the request was successful
        if response.status_code == 200:
            # extract relevant data from the Zoom API response
            token_data = response.json()
            current_token = token_data.get('access_token')
            # Set token expiry time (e.g., 1 hour from now)
            token_expiry = datetime.now() + timedelta(hours=1)
            ZoomToken.objects.update_or_create(defaults={'token': current_token, 'client_id': client_id, 'client_secret': client_secret, 'account_id':account_id, "expiry":token_expiry})
            return current_token, token_expiry
    except Exception as e:
        return e
    
def call_zoom_api(topic, type, start_time, userId, appointment):
    try:
        zoom_credentials = ZoomToken.objects.first()
        if zoom_credentials.token:
            token = zoom_credentials.token            

        # Define the headers
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {token}'
        }
        # define params
        params = {
            "userId": userId
        }
 
        # Define the data to be sent to the Zoom API
        data = {
            "topic": topic,
            "type": type,
            "start_time": start_time,
            "settings": {
                "host_video": True,
                "participant_video": True,
                "join_before_host": True,
                "mute_upon_entry": True,
                "watermark": False,
                "audio": "voip",
                "auto_recording": "none",
                "waiting_room": False
            }
        }
        # make the post request to create a meeting
        response = requests.post('https://api.zoom.us/v2/users/me/meetings', headers=headers, json=data, params=params)                
        # check if the request was successful
        if response.status_code == 201:
            # extract relevant data from the Zoom API response
            zoom_data = response.json()
            meeting_id = zoom_data.get('id')
            join_url = zoom_data.get('join_url')
            password = zoom_data.get('password')
            # save meeting data to the Zoom table with appointment_id
            zoom_instance = Zoom.objects.create(
                appointment_id=appointment.id,
                meeting_id=meeting_id,
                join_url=join_url,
                password=password,
            )

            return zoom_instance
        else:
            token, expiry = generate_token()
            call_zoom_api(topic, type, start_time, userId, appointment)
    except Exception as e:       
        token, expiry = generate_token()
        call_zoom_api(topic, type, start_time, userId, appointment)
        return e
    
def create_meeting(topic, type, start_time, userId, appointment):
    try:
        response = call_zoom_api(topic, type, start_time, userId, appointment)
        return response
       
    except Exception as e:
        return e
