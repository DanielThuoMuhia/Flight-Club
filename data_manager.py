# Import necessary modules
import requests  # For making HTTP requests to APIs
from requests.auth import HTTPBasicAuth  # For basic HTTP authentication
from pprint import pprint  # For pretty-printing JSON or dictionary data for readability
import os  # For accessing environment variables like API credentials
from dotenv import load_dotenv  # For loading environment variables from a .env file

# Load environment variables from the .env file into the script
load_dotenv()

# Define Sheety API endpoints from environment variables
sheety_endpoint = os.getenv("SHEETY_ENDPOINT")  # Endpoint for destination data
sheety_user_endpoint = os.getenv("SHEETY_USER_END_POINT")  # Endpoint for user data

# Retrieve Sheety API credentials from environment variables
sheety_username = os.getenv("SHEETY_USERNAME")  # Username for API authentication
sheety_password = os.getenv("SHEETY_PASSWORD")  # Password for API authentication

# Define a class to manage data-related tasks such as fetching and updating information
class DataManager:

    def __init__(self):
        """Initialize the DataManager with API credentials and authentication setup."""
        
        self.user = sheety_username  # API username for Sheety
        self.password = sheety_password  # API password for Sheety
        self.authorization = HTTPBasicAuth(self.user, self.password)  # Set up basic authentication for API requests
        self.destination_data = {}  # Initialize an empty dictionary to hold fetched destination data

    def get_destination_data(self):
        """
        Fetch the destination data from the Sheety API.

        Returns:
            dict: A dictionary containing the destination data from the Sheety API.
        """
        
        # Send a GET request to the Sheety API, including authentication
        response = requests.get(url=sheety_endpoint, auth=self.authorization)
        response.raise_for_status()  # Check for any request errors and raise exceptions if found

        # Parse the JSON response and store the 'prices' data (destination details)
        data = response.json()
        self.destination_data = data["prices"]  # Save destination data to an instance variable
        
        # Return the fetched destination data
        return self.destination_data

    def update_destination_codes(self):
        """
        Update IATA codes for each city in the destination data.

        Iterates through each city in destination data and updates its IATA code
        in the Sheety API using a PUT request.
        """
        
        # Loop through each city in the destination data
        for city in self.destination_data:
            # Prepare the updated data payload with the new IATA code
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]  # Replace with current city's IATA code
                }
            }
            
            # Send a PUT request to update the city's IATA code in the Sheety database
            response = requests.put(url=f"{sheety_endpoint}/{city['id']}", json=new_data, auth=self.authorization)
            response.raise_for_status()  # Raise an error if the request fails

            # Print the response to confirm a successful update
            updated_data = response.text
            print(updated_data)

    def get_customers_emails(self):
        """
        Fetch customer email data from the Sheety API.

        Returns:
            list: A list of dictionaries, each containing details of a customer (e.g., email).
        """
        
        # Send a GET request to the Sheety API to fetch user data
        response = requests.get(url=sheety_user_endpoint)
        response.raise_for_status()  # Raise an error if the request fails

        # Parse the JSON response and store user data
        data = response.json()
        # pprint(data)  # Uncomment to pretty-print data for debugging

        # Extract customer data (email and details) and store it in an instance variable
        self.customer_data = data["users"]
        
        # Return the list of customer data
        return self.customer_data


# Example usage:
# data_manager = DataManager()
# print(data_manager.get_customers_emails())
