# Import necessary modules
import requests  # For making HTTP requests
from requests.auth import HTTPBasicAuth  # For basic authentication in HTTP requests
from pprint import pprint  # For pretty-printing JSON or dictionary data
import os  # For accessing environment variables
from dotenv import load_dotenv  # For loading environment variables from a .env file

# Load environment variables from .env file
load_dotenv()

# Define Sheety API endpoint
SHEETY_ENDPOINT = "https://api.sheety.co/a8d6b46af04b86ae5ed448d65b91850f/flightDeals/prices"

# Retrieve Sheety API credentials from environment variables
sheety_username = os.getenv("SHEETY_USERNAME")
sheety_password = os.getenv("SHEETY_PASSWORD")

# Define a class to manage data-related tasks
class DataManager:

    def __init__(self):
        """Initialize the DataManager with API credentials and authentication."""
        
        self.user = sheety_username  # Username for Sheety API
        self.password = sheety_password  # Password for Sheety API
        self.authorization = HTTPBasicAuth(self.user, self.password)  # Set up Basic Auth
        self.destination_data = {}  # Initialize an empty dictionary to store destination data

    def get_destination_data(self):
        """
        Fetch the destination data from Sheety API.
        
        Returns:
            dict: A dictionary containing the destination data from the Sheety API.
        """
        
        # Send a GET request to the Sheety API with authentication
        response = requests.get(url=SHEETY_ENDPOINT, auth=self.authorization)
        response.raise_for_status()  # Raise an error if the request fails

        # Parse the JSON response and store the 'prices' data
        data = response.json()
        self.destination_data = data["prices"]
        
        # Return the destination data
        return self.destination_data

    def update_destination_codes(self):
        """
        Update IATA codes for each city in the destination data.
        
        Iterates through each city in destination data and updates its IATA code
        in the Sheety API using a PUT request.
        """
        
        # Loop through each city in the destination data
        for city in self.destination_data:
            # Prepare the updated data with the new IATA code
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            
            # Send a PUT request to update the city's IATA code in Sheety
            response = requests.put(url=f"{SHEETY_ENDPOINT}/{city['id']}", json=new_data, auth=self.authorization)
            response.raise_for_status()  # Raise an error if the request fails

            # Print the response to confirm successful update
            updated_data = response.text
            print(updated_data)
