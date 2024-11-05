# Import necessary modules
import os  # For accessing environment variables
from twilio.rest import Client  # For interacting with Twilio's API
from dotenv import load_dotenv  # For loading environment variables from a .env file
import smtplib

# Load environment variables from .env file to keep sensitive information secure
load_dotenv()

twilio_sid = os.getenv('TWILIO_ACCOUNT_SID')
twilio_auth_token = os.getenv("TWILIO_AUTH_TOKEN")


# Define a class to manage notifications using Twilio
class NotificationManager:

    def __init__(self):
        """
        Initialize the NotificationManager by creating a Twilio Client with account SID and auth token.
        """
          
         # Retrieve environment variables only once
        self.twilio_number = os.getenv("TWILIO_NUMBER") 
        self.my_number = os.getenv("MY_NUMBER")  
        self. my_email = os.getenv("MY_EMAIL")
        self.my_app_password = os.getenv("MY_APP_PASSWORD")
        self.email_provider_smtp_address = os.getenv("EMAIL_PROVIDER_SMTP_ADDRESS")
        self.port = os.getenv("PORT")

        # Set up Twilio Client and SMTP connection
        self.client = Client(twilio_sid, twilio_auth_token)
        self.connection = smtplib.SMTP(self.email_provider_smtp_address, self.port)

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
            from_=self.twilio_number,  # Twilio-provided number
            body=message_body,  # Message content
            to=self.my_number  # Recipient's WhatsApp number
        )

        # Output the message SID to confirm successful message delivery
        print(message.sid)

    def send_emails(self, email_list, email_body):
        with self.connection as connection:
            connection.starttls()  # Secure the connection
            connection.login(user=self.my_emailL, password=self.my_app_password) 
            for email in email_list:
                connection.sendmail(
                    from_addr=self.my_email,
                    to_addrs=email,
                    msg=f"Subject:New Low Price Flight!\n\n{email_body}".encode('utf-8')
                )


