# Import required modules
import os  # For accessing environment variables
from dotenv import load_dotenv  # For loading environment variables from a .env file
import requests  # For making HTTP requests
from datetime import datetime as dt  # For handling date and time operations

# Load environment variables from .env file
load_dotenv()

# Define Amadeus API endpoints for authentication, city IATA lookup, and flight offers
TOKEN_ENDPOINT = "https://test.api.amadeus.com/v1/security/oauth2/token"
IATA_ENDPOINT = "https://test.api.amadeus.com/v1/reference-data/locations/cities"
FLIGHT_ENDPOINT = "https://test.api.amadeus.com/v2/shopping/flight-offers"

# Retrieve Amadeus API credentials from environment variables
amadeus_api_key = os.getenv("AMADEUS_API_KEY")
amadeus_api_secret = os.getenv("AMADEUS_SECRET_KEY")

# Define a class to handle flight search operations using the Amadeus API
class FlightSearch:

    def __init__(self):
        """
        Initialize the FlightSearch object by setting API credentials and obtaining an access token.
        """
        
        self.api_key = amadeus_api_key  # Store API key
        self.api_secret = amadeus_api_secret  # Store API secret
        self.token = self.get_new_token()  # Obtain a new token for API access

    def get_new_token(self):
        """
        Obtain a new access token from the Amadeus API using client credentials.
        
        Returns:
            str: The access token needed to make API requests.
        """
        
        # Prepare the request body for the token request
        body = {
            "grant_type": "client_credentials",
            "client_id": amadeus_api_key,
            "client_secret": amadeus_api_secret
        }

        # Set the header to indicate form-encoded content
        header = {
            "content-type": "application/x-www-form-urlencoded"
        }

        # Send a POST request to the Amadeus token endpoint to retrieve the access token
        response = requests.post(url=TOKEN_ENDPOINT, headers=header, data=body)
        response.raise_for_status()  # Raise an error if the request fails

        # Extract the access token from the JSON response
        data = response.json()['access_token']
        return data

    def get_destination_code(self, city_name):
        """
        Retrieve the IATA code for a given city name using the Amadeus API.
        
        Args:
            city_name (str): Name of the city for which to find the IATA code.

        Returns:
            str: The IATA code of the city, or a message if the code is not found.
        """
        
        print(f"Using this token to get destination {self.token}")
        headers = {"Authorization": f"Bearer {self.token}"}

        # Set up query parameters for the city IATA code search
        query = {
            "keyword": city_name,
            "max": "2",
            "include": "AIRPORTS",
        }

        # Send a GET request to the IATA endpoint with the query parameters
        response = requests.get(url=IATA_ENDPOINT, headers=headers, params=query)
        print(f"Status code {response.status_code}. Airport IATA: {response.text}")

        try:
            # Attempt to extract the IATA code from the JSON response
            code = response.json()["data"][0]['iataCode']
        except IndexError:
            # Handle case where no IATA code is found in the response
            print(f"IndexError: No airport code found for {city_name}.")
            return "N/A"
        except KeyError:
            # Handle case where expected data keys are missing
            print(f"KeyError: No airport code found for {city_name}.")
            return "Not Found"

        return code

    def check_flights(self, origin_city_code, destination_city_code, from_time, to_time):
        """
        Search for flights between two cities within a specified date range.
        
        Args:
            origin_city_code (str): IATA code of the departure city.
            destination_city_code (str): IATA code of the destination city.
            from_time (datetime): Departure date.
            to_time (datetime): Return date.

        Returns:
            dict or None: JSON data containing flight offers, or None if an error occurred.
        """
        
        headers = {"Authorization": f"Bearer {self.token}"}

        # Set up query parameters for the flight search
        query = {
            "originLocationCode": origin_city_code,
            "destinationLocationCode": destination_city_code,
            "departureDate": from_time.strftime("%Y-%m-%d"),
            "returnDate": to_time.strftime("%Y-%m-%d"),
            "adults": 1,
            "nonStop": "true",  # Only include non-stop flights
            "currencyCode": "GBP",  # Display prices in British Pounds
            "max": "10",  # Limit the number of results to 10
        }

        # Send a GET request to the flight offers endpoint with the specified parameters
        response = requests.get(url=FLIGHT_ENDPOINT, params=query, headers=headers)
        
        # Check if the response status code indicates a successful request
        if response.status_code != 200:
            # Log error details if the request was unsuccessful
            print(f"check_flights() response code: {response.status_code}")
            print("There was a problem with the flight search.\n"
                  "For details on status codes, check the API documentation:\n"
                  "https://developers.amadeus.com/self-service/category/flights/api-doc/flight-offers-search/api"
                  "-reference")
            print("Response body:", response.text)
            return None

        # Return the JSON response containing flight data
        return response.json()

    

