import sqlite3

# Function to get all air quality data
def get_all_air_quality_data():
    try:
        # Connect to SQLite database
        conn = sqlite3.connect('air_quality_30_6-22_9.db')
        c = conn.cursor()

        # Query to get information about city and air quality parameters
        c.execute('''
            SELECT City.city_name, City.latitude, City.longitude, AirQualityData.dt, 
                   AirQualityData.co, AirQualityData.no2, AirQualityData.o3, AirQualityData.so2, 
                   AirQualityData.pm2_5, AirQualityData.pm10, AirQualityData.nh3
            FROM AirQualityData
            JOIN City ON AirQualityData.city_id = City.id
        ''')

        # Get all results
        rows = c.fetchall()

        # Show results
        for row in rows:
            city_name = row[0] or 'N/A'
            lat = row[1] or 'N/A'
            lon = row[2] or 'N/A'
            timestamp = row[3] or 'N/A'
            co = row[4] if row[4] is not None else 'N/A'
            no2 = row[5] if row[5] is not None else 'N/A'
            o3 = row[6] if row[6] is not None else 'N/A'
            so2 = row[7] if row[7] is not None else 'N/A'
            pm2_5 = row[8] if row[8] is not None else 'N/A'
            pm10 = row[9] if row[9] is not None else 'N/A'
            nh3 = row[10] if row[10] is not None else 'N/A'

            # Print results with formatting
            print(f"City: {city_name}, Lat: {lat}, Lon: {lon}, Timestamp: {timestamp}")
            print(f"CO: {co}, NO2: {no2}, O3: {o3}, SO2: {so2}")
            print(f"PM2.5: {pm2_5}, PM10: {pm10}, NH3: {nh3}")
            print('---------------------------------------------')

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    get_all_air_quality_data()
