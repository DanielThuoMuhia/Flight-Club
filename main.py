import time
from datetime import datetime, timedelta
from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import FlightData
from notification_manager import NotificationManager

# ==================== Set up the Flight Search ====================

# Create instances of the necessary classes
data_manager = DataManager()  # To handle data management tasks
sheet_data = data_manager.get_destination_data()  # Fetch destination data from the Google Sheet
flight_search = FlightSearch()  # To search for flights
notification_manager = NotificationManager()  # To handle notifications

# Set your origin airport IATA code
ORIGIN_CITY_IATA = "LON"

# ==================== Update the Airport Codes in Google Sheet ====================

# Loop through the sheet data to update IATA codes
for row in sheet_data:
    if row["iataCode"] == "":
        # Get and set the destination IATA code if it's missing
        row["iataCode"] = flight_search.get_destination_code(row["city"])
        # Slowing down requests to avoid rate limits
        time.sleep(2)

# Print the updated sheet data for debugging
print(f"sheet_data:\n {sheet_data}")

# Update the destination data in the DataManager
data_manager.destination_data = sheet_data
data_manager.update_destination_codes()  # Send updated data back to Google Sheets

# ==================== Search for Flights ====================

# Define the search period: tomorrow and six months from today
tomorrow = datetime.now() + timedelta(days=1)
six_month_from_today = datetime.now() + timedelta(days=(6 * 30))

# Loop through each destination in the sheet data to search for flights
for destination in sheet_data:
    print(f"Getting flights for {destination['city']}...")
    try:
        # Check for flights from the origin to the destination within the specified date range
        flights = flight_search.check_flights(
            ORIGIN_CITY_IATA,
            destination["iataCode"],
            from_time=tomorrow,
            to_time=six_month_from_today
        )

        # If there are flight results
        if flights:
            # Find the cheapest flight from the available options
            cheapest_flight = FlightData.find_cheapest_flight(flights)

            # Check if we have valid flight data and price
            if cheapest_flight and cheapest_flight.price != "N/A":
                print(f"{destination['city']}: £{cheapest_flight.price}")

                # Notify if a lower price flight is found
                if cheapest_flight.price < destination["lowestPrice"]:
                    print(f"Lower price flight found to {destination['city']}!")
                    notification_manager.send_whatsapp(
                        message_body=f"Low price alert! Only £{cheapest_flight.price} to fly "
                                     f"from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}, "
                                     f"on {cheapest_flight.out_date} until {cheapest_flight.return_date}."
                    )
                else:
                    print(f"No lower price found for {destination['city']}.")
                    notification_manager.send_whatsapp(
                        message_body=f"No lower price found for flights to {destination['city']}. Current price: £{cheapest_flight.price}."
                    )
            else:
                # Handle case where no valid flight data is available
                print(f"No valid flight data available for {destination['city']}.")
                notification_manager.send_whatsapp(
                    message_body=f'No valid flight data available for {destination["city"]}.'
                )
        else:
            # Handle case where no flight data is returned
            print(f"No flight data available for {destination['city']}.")
            notification_manager.send_whatsapp(
                message_body=f'No flight data available for {destination["city"]}.'
            )

    except Exception as e:
        # Catch and log any exceptions that occur during the flight search
        print(f"Error occurred while fetching flights for {destination['city']}: {str(e)}")
        notification_manager.send_whatsapp(
            message_body=f"Error occurred while fetching flights for {destination['city']}: {str(e)}"
        )
