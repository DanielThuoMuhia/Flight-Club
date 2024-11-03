# Define a class to store flight information and find the cheapest flight from data
class FlightData:

    def __init__(self, price, origin_airport, destination_airport, out_date, return_date):
        """
        Initialize the FlightData object with details of a flight.
        
        Args:
            price (float): Price of the flight.
            origin_airport (str): IATA code of the departure airport.
            destination_airport (str): IATA code of the destination airport.
            out_date (str): Departure date in 'YYYY-MM-DD' format.
            return_date (str): Return date in 'YYYY-MM-DD' format.
        """
        
        self.price = price
        self.origin_airport = origin_airport
        self.destination_airport = destination_airport
        self.out_date = out_date
        self.return_date = return_date

    @staticmethod
    def find_cheapest_flight(data):
        """
        Find and return the cheapest flight from a given data set.

        Args:
            data (dict): Dictionary containing flight data from an API response.

        Returns:
            FlightData: An instance of FlightData with the details of the cheapest flight.
        """
        
        # Handle case when data is None or contains no flight information
        if data is None or not data['data']:
            print("No flight data")
            return FlightData("N/A", "N/A", "N/A", "N/A", "N/A")

        # Extract details from the first flight as a starting point
        first_flight = data['data'][0]
        lowest_price = float(first_flight["price"]["grandTotal"])  # Initial lowest price
        origin = first_flight["itineraries"][0]["segments"][0]["departure"]["iataCode"]
        destination = first_flight["itineraries"][0]["segments"][0]["arrival"]["iataCode"]
        out_date = first_flight["itineraries"][0]["segments"][0]["departure"]["at"].split("T")[0]
        return_date = first_flight["itineraries"][1]["segments"][0]["departure"]["at"].split("T")[0]

        # Create a FlightData instance with the initial flight details for comparison
        cheapest_flight = FlightData(lowest_price, origin, destination, out_date, return_date)

        # Iterate through each flight in the data to find the cheapest option
        for flight in data["data"]:
            price = float(flight["price"]["grandTotal"])  # Convert price to float for comparison
            
            # Update if the current flight has a lower price than the previous cheapest
            if price < lowest_price:
                lowest_price = price
                origin = flight["itineraries"][0]["segments"][0]["departure"]["iataCode"]
                destination = flight["itineraries"][0]["segments"][0]["arrival"]["iataCode"]
                out_date = flight["itineraries"][0]["segments"][0]["departure"]["at"].split("T")[0]
                return_date = flight["itineraries"][1]["segments"][0]["departure"]["at"].split("T")[0]
                cheapest_flight = FlightData(lowest_price, origin, destination, out_date, return_date)
                
                # Print the current lowest price and destination for reference
                print(f"Lowest price to {destination} is £{lowest_price}")

        # Return the FlightData instance with the cheapest flight details
        return cheapest_flight

    

