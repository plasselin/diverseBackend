# views.py
import os
import openai
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from openai import OpenAI
import logging
from django.conf import settings
import requests
import time
import traceback
import io


openai.api_key = settings.OPENAI_API_KEY

logging.basicConfig(level=logging.DEBUG)
client = OpenAI(
    api_key=settings.OPENAI_API_KEY,
    organization=settings.OPENAI_ORGANIZATION
)


@csrf_exempt
def chat_completion(request):
    if request.method == 'POST':
        try:
            logging.debug(f"Request body: {request.body}")

            data = json.loads(request.body)
            logging.debug(f"Parsed data: {data}")

            # Extract values from the request body
            user_message = data.get('message', {}).get('text', '')
            is_voice_enabled = data.get('message', {}).get('isVoiceEnabled', False)
            temperature = data.get('message', {}).get('temperature', 0.5)  # Default temperature
            model = data.get('message', {}).get('model', 'gpt-4')  # Default to 'gpt-4'
            message_index = data.get('message', {}).get('index', int(time.time()))  # Use message index or timestamp
            logging.debug(f"User message: {user_message}, Voice enabled: {is_voice_enabled}, Message index: {message_index}, Temperature: {temperature}, Model: {model}")

            if not user_message:
                logging.error("User message is empty")
                return JsonResponse({'error': 'User message is empty'}, status=400)

            # Call OpenAI GPT completion with the provided model and temperature
            max_tokens = 100 if is_voice_enabled else None
            response = client.chat.completions.create(
                model=model,  # Use the dynamic model from the request
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": user_message}
                ],
                temperature=temperature,  # Use the dynamic temperature from the request
                max_tokens=max_tokens
            )

            logging.debug(f"OpenAI text response: {response}")

            assistant_response = response.choices[0].message.content

            # If voice is enabled, generate TTS audio and send both text and audio
            if is_voice_enabled:
                tts_response = client.audio.speech.create(
                    model="tts-1",  # Fixed model for TTS
                    voice="alloy",
                    input=assistant_response
                )

                # Save the TTS audio file
                audio_dir = os.path.join(settings.BASE_DIR, 'static', 'audio')
                if not os.path.exists(audio_dir):
                    os.makedirs(audio_dir)

                audio_file_path = f"static/audio/output_{message_index}.mp3"
                tts_response.stream_to_file(audio_file_path)

                # Clean up old audio files (keep only the latest 10)
                audio_files = sorted(
                    [f for f in os.listdir(audio_dir) if f.endswith('.mp3')],
                    key=lambda x: os.path.getmtime(os.path.join(audio_dir, x))
                )
                if len(audio_files) > 10:
                    files_to_delete = audio_files[:-10]
                    for file_name in files_to_delete:
                        file_path = os.path.join(audio_dir, file_name)
                        os.remove(file_path)
                        logging.debug(f"Deleted old audio file: {file_path}")

                logging.debug(f"OpenAI TTS response saved to {audio_file_path}")

                audio_file_absolute_url = request.build_absolute_uri(f'/static/audio/output_{message_index}.mp3')
                return JsonResponse({
                    'text': assistant_response,
                    'audio_file': audio_file_absolute_url,
                    'sender': 'assistant'
                })

            return JsonResponse({
                'text': assistant_response,
                'sender': 'assistant'
            })

        except Exception as e:
            logging.error(f"Error during completion: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Only POST method is allowed'}, status=405)



@csrf_exempt
def transcribe_audio(request):
    if request.method == 'POST':
        try:
            # Print request data for debugging purposes
            print(f"Request POST data: {request.POST}")
            print(f"Request FILES: {request.FILES}")

            # Get the audio file from the request
            audio_file = request.FILES.get('file')

            if not audio_file:
                print("No audio file provided")
                return JsonResponse({'error': 'No audio file provided'}, status=400)

            # Print file details for debugging
            print(f"Audio file: {audio_file.name}, size: {audio_file.size}")

            # Define the path where the file will be saved
            audio_dir = os.path.join(settings.BASE_DIR, 'static', 'audio')
            if not os.path.exists(audio_dir):
                os.makedirs(audio_dir)

            # Create a unique filename for the input file
            file_name = f"input_{audio_file.name}"
            file_path = os.path.join(audio_dir, file_name)

            # Save the file to the audio folder
            with open(file_path, 'wb+') as destination:
                for chunk in audio_file.chunks():
                    destination.write(chunk)

            print(f"File saved at: {file_path}")

            # Open the saved file and send it to the OpenAI Whisper API
            with open(file_path, 'rb') as stored_audio_file:
                transcript = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=stored_audio_file
                )

            # Access the 'text' property from the transcript object
            transcription_text = transcript.text

            # Print transcription result for debugging
            print(f"Transcription result: {transcription_text}")

            # Return the transcribed text and set sender to 'user'
            return JsonResponse({
                'text': transcription_text,
                'sender': 'user'
            })

        except Exception as e:
            # Print the error and stack trace to the console
            print(f"Error during transcription: {str(e)}")
            print(traceback.format_exc())
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Only POST method is allowed'}, status=405)
