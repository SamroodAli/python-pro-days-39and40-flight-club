from data_manager import DataManager
from flight_search import FlightSearch
from datetime import datetime, timedelta
from notification_manager import NotificationManager

# Instances needed
# To manage google sheets data
data_manager = DataManager()
# To search for destination iata codes and flights
flight_search = FlightSearch()
# To alert user via sms using Twilio api
notification_manager = NotificationManager()

sheet_data = data_manager.get_sheets_data()

if sheet_data[0]["iataCode"] == "":
    for row in sheet_data:
        row["iataCode"] = flight_search.get_iata_code(row["city"])
    # Update sheets data
    data_manager.sheets_data = sheet_data
    data_manager.update_sheets_data()


# Get dates
tomorrow = datetime.now() + timedelta(days=1)
six_months_from_now = tomorrow + timedelta(days=6*30)

# Flight constants
origin_city_code = "LON"
flight_data_currency = "GBP"

for destination in sheet_data:
    flight = flight_search.check_flights(
        origin_city_code=origin_city_code,
        destination_city_code=destination["iataCode"],
        from_time=tomorrow,
        to_time=six_months_from_now,
        curr=flight_data_currency
    )
    if flight is not None:
        message = f"Flight deal alert\n Only {flight_data_currency} {flight['price']} to fly from {flight['origin_city']}-{flight['origin_airport']} to {flight['destination_city']}-{flight['destination_airport']}, from {flight['travel_date']} to {flight['return_date']}."
        if flight["stop_overs"] > 0:
            message += f"\nThe flight has {flight['stop_overs']} stop over, via {flight['via_city']}"
        print(message)
    # if flight["price"] < destination["lowestPrice"]:
        # notification_manager.send_sms(message=f"Flight deal alert\n Only {flight_data_currency} {flight['price']} to fly from {flight['origin_city']}-{flight['origin_airport']} to {flight['destination_city']}-{flight['destination_airport']}, from {flight['travel_date']} to {flight['return_date']}")
