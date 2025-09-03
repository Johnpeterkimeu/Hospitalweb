import africastalking
from django.conf import settings

# Initialize with settings
africastalking.initialize(
    username=settings.AFRICASTALKING_USERNAME,
    api_key=settings.AFRICASTALKING_API_KEY
)

sms = africastalking.SMS
