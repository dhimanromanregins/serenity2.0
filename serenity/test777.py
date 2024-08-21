from gtts import gTTS
import os
from django.conf import settings

def synthesize_speech(text, filename):
    """
    Synthesize speech from the given text and save it to a file.
    """
    # Create a gTTS object
    tts = gTTS(text=text, lang='en')

    # Save the speech to a file in the media folder
    media_path = os.path.join(settings.MEDIA_ROOT, 'text-to-speech', filename)
    os.makedirs(os.path.dirname(media_path), exist_ok=True)
    tts.save(media_path)

    return media_path


import pygame
import time

def play_audio(file_path):
    """
    Play the audio file specified by file_path.
    """
    # Initialize pygame mixer
    pygame.mixer.init()

    # Load and play the MP3 file
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

    # Wait until the audio has finished playing
    while pygame.mixer.music.get_busy():
        time.sleep(1)

audio_file_path = synthesize_speech("This is a test.", "test.mp3")

play_audio(audio_file_path)
