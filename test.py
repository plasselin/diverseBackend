import os
import django
from django.test import RequestFactory
from chatapi.views import tts_request

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject.settings')
django.setup()

# Create an instance of RequestFactory
factory = RequestFactory()

# Simulate a POST request with required data
request = factory.post('/api/tts/', {
    'text': 'This is a test of the TTS system from the Django shell.',
    'guidance': 3.0,
    'top_p': 0.95
})

# Call the tts_request view and capture the response
response = tts_request(request)

# Print the response content
print(response.content)
