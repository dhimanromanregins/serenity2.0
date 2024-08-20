import os
from google.cloud import texttospeech_v1 as tts
from google.oauth2 import service_account
from django.conf import settings
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
print(BASE_DIR, '========')
def synthesize_speech(text, filename, voice_name):
    # Path to your service account key file
    SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, 'crafty-calling-431608-f5-0e62b133091c.json')

    # Load credentials from the service account key file
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE
    )

    # Create a client using the credentials
    client = tts.TextToSpeechClient(credentials=credentials)

    # Define the text input and voice parameters
    input_text = tts.SynthesisInput(text=text)
    voice = tts.VoiceSelectionParams(
        language_code="en-US", name=voice_name
    )
    audio_config = tts.AudioConfig(
        audio_encoding=tts.AudioEncoding.MP3
    )

    # Synthesize speech
    response = client.synthesize_speech(
        input=input_text, voice=voice, audio_config=audio_config
    )

    # Save the audio content to a file in the media folder
    media_path = os.path.join(settings.MEDIA_ROOT, 'text-to-speech', filename)
    os.makedirs(os.path.dirname(media_path), exist_ok=True)
    with open(media_path, "wb") as out:
        out.write(response.audio_content)

    return media_path

