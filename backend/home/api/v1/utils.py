from rest_framework.response import Response
from rest_framework import status
import requests
from users.models import Zoom
from datetime import datetime, timedelta
import os
import base64
#call zoom api to create meeting

client_id = os.environ.get('CLIENT_ID')
client_secret = os.environ.get('CLIENT_SECRET')
account_id = os.environ.get('ACCOUNT_ID')

# Global variable to store the token and its expiration time
current_token = None
token_expiry = None

def generate_token():
    global current_token, token_expiry
    # check if the token exists and is not expired
    if current_token and token_expiry > datetime.now():
        return current_token
    try:
        auth = f'{client_id}:{client_secret}'
        # encode the client_id and client_secret to base64
        encoded_auth = base64.b64encode(auth.encode('utf-8')).decode('utf-8')
        print("encoded_auth", encoded_auth)
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
        print("response", response)
        # check if the request was successful
        if response.status_code == 200:
            # extract relevant data from the Zoom API response
            token_data = response.json()
            current_token = token_data.get('access_token')
            # Set token expiry time (e.g., 1 hour from now)
            token_expiry = datetime.now() + timedelta(hours=1)
            return current_token
    except Exception as e:
        print("error", e)
        return e


def create_meeting(topic, type, start_time, appointment, token, userId):
    try:
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
        print("response", response)
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
        
    except Exception as e:
        return e    


    


