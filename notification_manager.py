# Import necessary modules
import os  # For accessing environment variables
from twilio.rest import Client  # For interacting with Twilio's API
from dotenv import load_dotenv  # For loading environment variables from a .env file

# Load environment variables from .env file to keep sensitive information secure
load_dotenv()

# Retrieve Twilio credentials and phone numbers from environment variables
twilio_sid = os.getenv('TWILIO_ACCOUNT_SID')
twilio_auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_number = os.getenv("TWILIO_NUMBER")  # Twilio number (from which messages are sent)
my_number = os.getenv("MY_NUMBER")  # Your phone number (destination for messages)

# Define a class to manage notifications using Twilio
class NotificationManager:

    def __init__(self):
        """
        Initialize the NotificationManager by creating a Twilio Client with account SID and auth token.
        """
        self.client = Client(twilio_sid, twilio_auth_token)  # Twilio Client for sending messages

    # Optional: Use Twilio's WhatsApp Sandbox for WhatsApp messaging if SMS is not preferred or available
    # Learn more: https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn
    def send_whatsapp(self, message_body):
        """
        Send a WhatsApp message with the specified message body.

        Args:
            message_body (str): The content of the message to be sent.

        Returns:
            None
        """
        
        # Use Twilio's messaging service to send a WhatsApp message
        message = self.client.messages.create(
            from_=twilio_number,  # Twilio-provided number
            body=message_body,  # Message content
            to=my_number  # Recipient's WhatsApp number
        )

        # Output the message SID to confirm successful message delivery
        print(message.sid)



