#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import django
# from dotenv import load_dotenv
# Manually configure Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "silent_sea_44703.settings")

django.setup()

from modules.django_push_notifications.push_notifications.models import OneSignalApp, Notification


def main():
    #load environment variables from .env file
    # load_dotenv()
    # os.environ.setdefault(
    #     "DJANGO_SETTINGS_MODULE", "silent_sea_44703.settings"
    # )
    # import django
    # django.setup()
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    # Fetch app_id and api_key from the environment variables
    app_id = os.environ.get('ONESIGNAL_APP_ID')
    api_key = os.environ.get('ONESIGNAL_REST_API_KEY')

    if app_id and api_key:
        # Filter OneSignalApp instances with the provided app_id
        onesignal_apps = OneSignalApp.objects.filter(app_id=app_id)
        if onesignal_apps.exists():
            onesignal_app = onesignal_apps.first()  # Get the first instance
            # Update or create OneSignalApp instance with the fetched app_id and api_key
            onesignal_app.api_key = api_key
            onesignal_app.save()
            print("OneSignalApp entry updated successfully with the provided app_id")
        else:
            # Create a new OneSignalApp instance with the fetched app_id and api_key
            onesignal_app = OneSignalApp.objects.create(app_id=app_id, api_key=api_key)
            print("OneSignalApp entry created successfully with the provided app_id")
        
        # Update existing notifications to associate them with the correct OneSignalApp instance
        Notification.objects.filter(onesignal_app=None).update(onesignal_app=onesignal_app)
        print("Updated notifications to associate them with the correct OneSignalApp instance")
    else:
        print("Error: Could not fetch app_id and api_key from environment variables")

    execute_from_command_line(sys.argv)
    
if __name__ == '__main__':
    main()
