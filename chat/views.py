from decouple import config
from django.http import JsonResponse
from .models import Session, Recording
from .utils import start_and_save_recording, stop_and_save_recording, generate_agora_token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse

AGORA_APP_ID = config('AGORA_APP_ID')


# Create your views here.
@api_view(['POST'])
def start_session(request):
    """
    Start an Agora session and generate token, create session if needed.
    """
    if 'channel_name' not in request.data:
        return JsonResponse({'error': 'Channel name is required'}, status=400)
    if 'title' not in request.data:
        return JsonResponse({'error': 'Meeting title is required'}, status=400)

    response_data = generate_agora_token(request)
    return JsonResponse(response_data, status=200)


@api_view(['POST'])
def end_session(request, session_id):
    try:
        session = Session.objects.get(id=session_id, host=request.user)
        session.end_session()
        return Response({'message': 'Session ended successfully'}, status=200)
    except Session.DoesNotExist:
        return Response({'error': 'Session not found or you are not the host'}, status=404)


def start_recording_view(request, meeting_id):
    session = Session.objects.get(id=meeting_id)
    recording = start_and_save_recording(session)
    return JsonResponse({'status': 'recording started', 'recording_id': recording.id})


def stop_recording_view(request, recording_id):
    recording = Recording.objects.get(id=recording_id)
    updated_recording = stop_and_save_recording(recording)
    return JsonResponse({'status': 'recording stopped', 'file_url': updated_recording.file_url})
