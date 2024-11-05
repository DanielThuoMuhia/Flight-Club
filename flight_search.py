# Import required modules
import os  # For accessing environment variables securely
from dotenv import load_dotenv  # For loading environment variables from a .env file
import requests  # For making HTTP requests to APIs
from datetime import datetime as dt  # For handling date and time operations

# Load environment variables from .env file to avoid hardcoding sensitive information
load_dotenv()

# Retrieve API endpoints and credentials from environment variables
token_endpoint = os.getenv("TOKEN_ENDPOINT")
iata_endpoint = os.getenv("IATA_ENDPOINT")
flight_endpoint = os.getenv("FLIGHT_ENDPOINT")
amadeus_api_key = os.getenv("AMADEUS_API_KEY")  # Amadeus API key
amadeus_api_secret = os.getenv("AMADEUS_SECRET_KEY")  # Amadeus API secret

# Define a class to handle flight search operations using the Amadeus API
class FlightSearch:

    def __init__(self):
        """
        Initialize the FlightSearch object by setting API credentials and obtaining an access token.
        """
        self.api_key = amadeus_api_key  # Store API key for authentication
        self.api_secret = amadeus_api_secret  # Store API secret for authentication
        self.token = self.get_new_token()  # Obtain a new token for API access

    def get_new_token(self):
        """
        Obtain a new access token from the Amadeus API using client credentials.
        
        Returns:
            str: The access token needed to make authenticated API requests.
        """
        
        # Prepare the request body with required credentials for token retrieval
        body = {
            "grant_type": "client_credentials",
            "client_id": amadeus_api_key,
            "client_secret": amadeus_api_secret
        }

        # Set headers to indicate form-encoded content
        header = {
            "content-type": "application/x-www-form-urlencoded"
        }

        # Send a POST request to the Amadeus token endpoint to obtain access token
        response = requests.post(url=token_endpoint, headers=header, data=body)
        response.raise_for_status()  # Raise an error if the request fails

        # Extract the access token from the JSON response
        data = response.json()['access_token']
        return data

    def get_destination_code(self, city_name):
        """
        Retrieve the IATA code for a specified city name using the Amadeus API.
        
        Args:
            city_name (str): Name of the city for which to find the IATA code.

        Returns:
            str: The IATA code of the city, or an appropriate message if not found.
        """
        
        print(f"Using this token to get destination: {self.token}")
        headers = {"Authorization": f"Bearer {self.token}"}

        # Define query parameters for city IATA code lookup
        query = {
            "keyword": city_name,
            "max": "2",  # Limit to 2 results
            "include": "AIRPORTS",  # Include airport codes in the response
        }

        # Send a GET request to the IATA endpoint with the specified query
        response = requests.get(url=iata_endpoint, headers=headers, params=query)
        print(f"Status code {response.status_code}. Airport IATA: {response.text}")

        try:
            # Extract the IATA code from the response
            code = response.json()["data"][0]['iataCode']
        except IndexError:
            # Handle case where no airport code is found
            print(f"IndexError: No airport code found for {city_name}.")
            return "N/A"
        except KeyError:
            # Handle case where expected data keys are missing
            print(f"KeyError: No airport code found for {city_name}.")
            return "Not Found"

        return code

    def check_flights(self, origin_city_code, destination_city_code, from_time, to_time, is_direct=True):
        """
        Search for flights between two cities within a specified date range.
        
        Args:
            origin_city_code (str): IATA code of the departure city.
            destination_city_code (str): IATA code of the destination city.
            from_time (datetime): Date of departure.
            to_time (datetime): Date of return.
            is_direct (bool): Whether to limit to direct flights only.

        Returns:
            dict or None: JSON data containing flight offers, or None if an error occurred.
        """
        
        headers = {"Authorization": f"Bearer {self.token}"}

        # Set up query parameters for the flight search request
        query = {
            "originLocationCode": origin_city_code,
            "destinationLocationCode": destination_city_code,
            "departureDate": from_time.strftime("%Y-%m-%d"),  # Format date to YYYY-MM-DD
            "returnDate": to_time.strftime("%Y-%m-%d"),  # Format return date to YYYY-MM-DD
            "adults": 1,  # Number of passengers
            "nonStop": "true" if is_direct else "false",  # Direct flights only if specified
            "currencyCode": "GBP",  # Prices in British Pounds
            "max": "10",  # Limit the results to 10 flights
        }

        # Send a GET request to the flight offers endpoint with the specified parameters
        response = requests.get(url=flight_endpoint, params=query, headers=headers)
        
        # Check if the request was successful
        if response.status_code != 200:
            # Log details if the request failed
            print(f"check_flights() response code: {response.status_code}")
            print("There was a problem with the flight search.\n"
                  "For details on status codes, check the API documentation:\n"
                  "https://developers.amadeus.com/self-service/category/flights/api-doc/flight-offers-search/api"
                  "-reference")
            print("Response body:", response.text)
            return None

        # Return the JSON response containing flight data
        return response.json()
