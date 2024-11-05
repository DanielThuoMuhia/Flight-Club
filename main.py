import time
from datetime import datetime, timedelta
from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import FlightData
from notification_manager import NotificationManager

# ==================== Set up the Flight Search ====================

data_manager = DataManager()
sheet_data = data_manager.get_destination_data()
flight_search = FlightSearch()
notification_manager = NotificationManager()

# Set your origin airport
ORIGIN_CITY_IATA = "LON"

# ==================== Update the Airport Codes in Google Sheet ====================

for row in sheet_data:
    if not row.get("iataCode"):  # Check if iataCode is empty
        row["iataCode"] = flight_search.get_destination_code(row["city"])
        time.sleep(2)  # Slowing down requests to avoid rate limit

data_manager.destination_data = sheet_data
data_manager.update_destination_codes()

# ==================== Retrieve your customer emails ====================

customer_data = data_manager.get_customer_emails()
customer_email_list = [row["whatIsYourEmail?"] for row in customer_data]  # Ensure the key is correct

# ==================== Search for direct flights  ====================

tomorrow = datetime.now() + timedelta(days=1)
six_month_from_today = datetime.now() + timedelta(days=(6 * 30))

for destination in sheet_data:
    print(f"Getting direct flights for {destination['city']}...")
    flights = flight_search.check_flights(
        ORIGIN_CITY_IATA,
        destination["iataCode"],
        from_time=tomorrow,
        to_time=six_month_from_today
    )
    
    cheapest_flight = FlightData.find_cheapest_flight(flights)
    print(f"{destination['city']}: £{cheapest_flight.price}")
    time.sleep(2)

    # ==================== Search for indirect flight if N/A ====================

    if cheapest_flight.price == "N/A":
        print(f"No direct flight to {destination['city']}. Looking for indirect flights...")
        stopover_flights = flight_search.check_flights(
            ORIGIN_CITY_IATA,
            destination["iataCode"],
            from_time=tomorrow,
            to_time=six_month_from_today,
            is_direct=False
        )
        cheapest_flight = FlightData.find_cheapest_flight(stopover_flights)
        print(f"Cheapest indirect flight price is: £{cheapest_flight.price}")

    # ==================== Send Notifications and Emails  ====================

    if cheapest_flight.price != "N/A" and cheapest_flight.price < destination["lowestPrice"]:
        # Customize the message depending on the number of stops
        if cheapest_flight.stops == 0:
            message = (f"Low price alert! Only GBP {cheapest_flight.price} to fly direct "
                        f"from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}, "
                        f"on {cheapest_flight.out_date} until {cheapest_flight.return_date}.")
        else:
            message = (f"Low price alert! Only GBP {cheapest_flight.price} to fly "
                        f"from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}, "
                        f"with {cheapest_flight.stops} stop(s) "
                        f"departing on {cheapest_flight.out_date} and returning on {cheapest_flight.return_date}.")

        print(f"Check your email. Lower price flight found to {destination['city']}!")

        # Send notifications (comment out if not needed)
        # notification_manager.send_sms(message_body=message)  # Uncomment if SMS is needed
        notification_manager.send_whatsapp(message_body=message)

        # Send emails to everyone on the list
        notification_manager.send_emails(email_list=customer_email_list, email_body=message)

