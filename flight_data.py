# Define a class to store flight information and find the cheapest flight from data
class FlightData:

    def __init__(self, price, origin_airport, destination_airport, out_date, return_date, stops):
        """
        Initialize the FlightData object with details of a flight.
        
        Args:
            price (float): Price of the flight.
            origin_airport (str): IATA code of the departure airport.
            destination_airport (str): IATA code of the destination airport.
            out_date (str): Departure date in 'YYYY-MM-DD' format.
            return_date (str): Return date in 'YYYY-MM-DD' format.
            stops (int): Number of stops (0 for direct, 1 or more for indirect flights).
        """
        self.price = price
        self.origin_airport = origin_airport
        self.destination_airport = destination_airport
        self.out_date = out_date
        self.return_date = return_date
        self.stops = stops

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
        if data is None or not data.get('data'):
            print("No flight data available.")
            return FlightData("N/A", "N/A", "N/A", "N/A", "N/A", "N/A")

        # Initialize with the first flight data for comparison
        first_flight = data['data'][0]
        lowest_price = float(first_flight["price"]["grandTotal"])
        origin = first_flight["itineraries"][0]["segments"][0]["departure"]["iataCode"]
        destination = first_flight["itineraries"][0]["segments"][-1]["arrival"]["iataCode"]
        out_date = first_flight["itineraries"][0]["segments"][0]["departure"]["at"].split("T")[0]
        return_date = first_flight["itineraries"][1]["segments"][0]["departure"]["at"].split("T")[0]
        nr_stops = len(first_flight["itineraries"][0]["segments"]) - 1

        # Create an initial FlightData object for the first flight
        cheapest_flight = FlightData(lowest_price, origin, destination, out_date, return_date, nr_stops)

        # Loop through each flight to find the cheapest one
        for flight in data["data"]:
            price = float(flight["price"]["grandTotal"])
            if price < lowest_price:
                lowest_price = price
                origin = flight["itineraries"][0]["segments"][0]["departure"]["iataCode"]
                destination

    

