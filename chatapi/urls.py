# urls.py
from django.urls import path
from .views import chat_completion, transcribe_audio

urlpatterns = [
    path('chat/completion/', chat_completion, name='chat_completion'),
    path('transcribe/', transcribe_audio, name='transcribe_audio'),
]
