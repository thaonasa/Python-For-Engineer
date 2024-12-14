import json
from datetime import datetime, timezone
import requests

api_key = "8b2842fb1cc137da505a5b35a17454b7"

# List of cities want to get data for
cities = ["Ha Noi", "Ho Chi Minh City", "Hai Phong", "Da Nang", "Hue", "Nha Trang", "Can Tho"]


def get_lat_lon(city_name, api_key):
    # Construct the Geocoding API request URL
    geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=1&appid={api_key}"

    # Send GET request to the Geocoding API
    geo_response = requests.get(geo_url)

    # Parse the JSON response
    geo_data = geo_response.json()

    # Check if the response contains data
    if geo_data:
        lat = geo_data[0]['lat']
        lon = geo_data[0]['lon']
        return lat, lon
    else:
        print(f"Could not find coordinates for {city_name}")
        return None, None


def get_air_pollution_data(lat, lon, api_key, city):
    # Construct the Air Pollution API request URL
    pollution_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"

    # Send GET request to the Air Pollution API
    pollution_response = requests.get(pollution_url)

    # Parse the JSON response
    pollution_data = pollution_response.json()
    pollution_data["city"] = city

    result_data = {
        "city": city
    }
    result_data.update(pollution_data)
    return result_data


# Function to convert UNIX timestamp to 'yyyy-mm-dd hh:mm:ss'
def convert_unix_to_datetime(unix_time):
    return datetime.fromtimestamp(unix_time, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S')


def save_json_to_file(json_list, file_name):
    for item in json_list:
        for entry in item["list"]:
            entry["dt"] = convert_unix_to_datetime(entry["dt"])
            if 'main' in entry:
                del entry['main']
            if 'components' in entry and 'no' in entry['components']:
                del entry['components']['no']
    with open(file_name, 'w') as json_file:
        json.dump(json_list, json_file, indent=1)


def main():
    json_list = []
    print(f"Air pollution data:")
    for city in cities:
        # Get latitude and longitude
        lat, lon = get_lat_lon(city, api_key)

        # If lat and lon were found, get air pollution data
        if lat is not None and lon is not None:
            json_list.append(get_air_pollution_data(lat, lon, api_key, city))

    save_json_to_file(json_list, 'air_quality_current.json')
    print("Done")


# Schedule the job every hour (singular)
#schedule.every(1).hour.do(fetch_and_store_data)

if __name__ == "__main__":
    main()