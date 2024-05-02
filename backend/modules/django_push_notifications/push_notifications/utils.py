import os
import requests
import json

APP_ID = os.environ.get('APP_ID')
REST_API_KEY = os.environ.get('REST_API_KEY')

def send_push_notification(ids,message_title,message_body, consult_time, appointment_date, doctor_name, zoom_link, zoom_meeting_id, zoom_passcode):
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
            print("url",url)
            response = requests.get(url, headers=headers)
            print("response",response)
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
                 "appointment_date":appointment_date,
                 "zoom_link":zoom_link,
                 "zoom_meeting_id":zoom_meeting_id,
                 "zoom_passcode":zoom_passcode
            },
            "contents": {"en": message_title}
            }
        print("DATA",data)
        url = "https://onesignal.com/api/v1/notifications"
        print("URL",url)
        headers = {
                "accept": "application/json",
                "content-type": "application/json",
                "Authorization": f"Basic {REST_API_KEY}"
            }
        res = requests.post(url, json=data, headers=headers)
        print("RES",res)
        var = res.json()
        #extract notification id from the response 
        notification_id = var.get('id')
        print("PUSH RESPONSE",var)
        return notification_id
    except Exception as e:
            print(e)