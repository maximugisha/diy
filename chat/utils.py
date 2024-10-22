from decouple import config
from agora_token_builder import RtcTokenBuilder
import time

from django.db import IntegrityError
from rest_framework.response import Response
import requests
from django.utils import timezone
from .models import Recording, Session

AGORA_APP_ID = config('AGORA_APP_ID')
AGORA_CUSTOMER_ID = config('AGORA_CUSTOMER_ID')
AGORA_CUSTOMER_SECRET = config('AGORA_CUSTOMER_SECRET')
AGORA_CHANNEL_NAME = config('AGORA_CHANNEL_NAME')  # Channel for the call
AGORA_APP_CERTIFICATE = config('AGORA_APP_CERTIFICATE')


# Helper to get Agora token
def generate_agora_token(request):
    # Get channel name and user information
    channel_name = request.data.get("channel_name")
    title = request.data.get("title")
    channel_name = channel_name.replace(" ", "-")
    uid = request.user.id  # Assuming JWT authentication returns the user object

    # Agora app credentials
    app_id = AGORA_APP_ID
    app_certificate = AGORA_APP_CERTIFICATE

    # Token expiration time (1 hour here)
    expiration_time_in_seconds = 3600
    current_timestamp = int(time.time())
    privilege_expired_ts = current_timestamp + expiration_time_in_seconds
    role = 1  # Role for broadcaster (1)

    # Generate Agora token
    token = RtcTokenBuilder.buildTokenWithUid(app_id, app_certificate, channel_name, uid, role, privilege_expired_ts)

    # Check if a session already exists for the given channel

    session, created = Session.objects.get_or_create(
        channel_name=channel_name,
        defaults={
            'host': request.user,
            'start_time': timezone.now(),
            'title': title,
        }
    )


# Return the token and the session info (session_id can also be used)
    return {
        'token': token,
        'uid': uid,
        'channel_name': channel_name,
        'session_id': session.id,
        'is_new_session': created,
        'title': title,
    }


# Acquire resource for recording
def acquire_recording(channel_name, uid):
    url = f"https://api.agora.io/v1/apps/{AGORA_APP_ID}/cloud_recording/acquire"
    headers = {
        "Authorization": f"Basic {AGORA_CUSTOMER_ID}:{AGORA_CUSTOMER_SECRET}",
        "Content-Type": "application/json"
    }
    payload = {
        "cname": channel_name,
        "uid": uid,
        "clientRequest": {}
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()


# Start recording
def start_recording(channel_name, uid, resource_id):
    url = f"https://api.agora.io/v1/apps/{AGORA_APP_ID}/cloud_recording/resourceid/{resource_id}/mode/mix/start"
    headers = {
        "Authorization": f"Basic {AGORA_CUSTOMER_ID}:{AGORA_CUSTOMER_SECRET}",
        "Content-Type": "application/json"
    }
    payload = {
        "cname": channel_name,
        "uid": uid,
        "clientRequest": {
            "recordingConfig": {
                "maxIdleTime": 120,
                "streamTypes": 2,  # Audio and Video
                "audioProfile": 1,
                "channelType": 1,  # Communication
                "videoStreamType": 0,  # High quality
            },
            "storageConfig": {
                "vendor": 1,  # 1 is for Agora's internal storage
                "region": "us",
                "bucket": "your-bucket",
                "accessKey": "your-access-key",
                "secretKey": "your-secret-key",
                "fileNamePrefix": ["recordings"]
            }
        }
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()


# Stop recording
def stop_recording(resource_id, sid):
    url = f"https://api.agora.io/v1/apps/{AGORA_APP_ID}/cloud_recording/resourceid/{resource_id}/sid/{sid}/mode/mix/stop"
    headers = {
        "Authorization": f"Basic {AGORA_CUSTOMER_ID}:{AGORA_CUSTOMER_SECRET}",
        "Content-Type": "application/json"
    }
    payload = {"cname": AGORA_CHANNEL_NAME, "uid": "12345"}
    response = requests.post(url, headers=headers, json=payload)
    return response.json()


# Start and save recording metadata
def start_and_save_recording(meeting):
    # Acquire resource
    resource_response = acquire_recording(AGORA_CHANNEL_NAME, '12345')
    resource_id = resource_response['resourceId']

    # Start recording
    start_response = start_recording(AGORA_CHANNEL_NAME, '12345', resource_id)
    sid = start_response['sid']

    # Save to Recording model
    recording = Recording.objects.create(
        meeting=meeting,
        resource_id=resource_id,
        sid=sid,
        start_time=timezone.now()
    )
    return recording


# Stop recording and update metadata
def stop_and_save_recording(recording):
    stop_response = stop_recording(recording.resource_id, recording.sid)

    # Assuming the stop response contains the file URL and duration
    recording.file_url = stop_response['serverResponse']['fileList'][0]['fileName']
    recording.end_time = timezone.now()
    recording.duration = recording.end_time - recording.start_time
    recording.save()

    return recording
