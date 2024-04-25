import os
import requests
import json

APP_ID = os.environ.get('APP_ID')
REST_API_KEY = os.environ.get('REST_API_KEY')

def send_push_notification(ids,message_title,message_body, consult_time, appointment_date, doctor_name):
    headers = {
                "accept": "application/json",
                "content-type": "application/json",
                # "Content-Type": "application/json",
                "Authorization": f"Basic {REST_API_KEY}"
            }
    try:
        subscription_ids = []
        external_user_ids=[]
        for id in ids:  
            url = f"https://api.onesignal.com/apps/{APP_ID}/users/by/external_id/{id}"
            # print("url",url)
            response = requests.get(url, headers=headers)
            data = response.json()
            if data.get('subscriptions',None):
                subscription_ids.extend( item["id"] for item in data['subscriptions'])
                external_user_ids.append(id) # append external user id
        if not subscription_ids:
            return
        print("subscription_ids",subscription_ids)
        data = {
            "app_id": APP_ID,
            "include_external_user_ids": external_user_ids, # include external user id
            # "include_player_ids": [sub_id for sub_id in subscription_ids],
            "include_player_ids": [sub_id for sub_id in subscription_ids],
            "target_channel": "push",
            "data": {
                 "message": message_body,
                 "doctor_name": doctor_name,
                 "consult_time":consult_time,
                 "appointment_date":appointment_date
            },
            "contents": {"en": message_title}
            }
        print("DATA",data)
        url = "https://onesignal.com/api/v1/notifications"
        headers = {
                "accept": "application/json",
                "content-type": "application/json",
                "Authorization": f"Basic {REST_API_KEY}"
            }
        res = requests.post(url, json=data, headers=headers)
        var = res.json()
        print("PUSH RESPONSE",var)
    except Exception as e:
            print(e)