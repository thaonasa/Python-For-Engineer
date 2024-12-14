import sqlite3
import json

# Connect to SQLite database
conn = sqlite3.connect('air_quality_30_6-22_9.db')
c = conn.cursor()

# Create City table
c.execute('''
CREATE TABLE IF NOT EXISTS City (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    city_name TEXT NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL
)
''')

# Create AirQualityData table
c.execute('''
CREATE TABLE IF NOT EXISTS AirQualityData (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    city_id INTEGER NOT NULL,
    co REAL,
    no2 REAL,
    o3 REAL,
    so2 REAL,
    pm2_5 REAL,
    pm10 REAL,
    nh3 REAL,
    dt TEXT NOT NULL,
    FOREIGN KEY (city_id) REFERENCES City(id)
)
''')

# Function to get city_id, add new city if it doesn't exist


def get_or_create_city_id(city_name, latitude, longitude):
    c.execute('SELECT id FROM City WHERE city_name = ?', (city_name,))
    row = c.fetchone()
    if row:
        return row[0]
    else:
        c.execute('INSERT INTO City (city_name, latitude, longitude) VALUES (?, ?, ?)',
                  (city_name, latitude, longitude))
        conn.commit()
        return c.lastrowid

# Function to insert data from JSON file into database


def insert_data_from_json(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)

    for record in data:
        city_name = record['city']
        latitude = record['coord']['lat']
        longitude = record['coord']['lon']
        city_id = get_or_create_city_id(city_name, latitude, longitude)

        for air_quality in record['list']:
            components = air_quality['components']
            co = components.get('co')
            no2 = components.get('no2')  # Added no2
            o3 = components.get('o3')
            so2 = components.get('so2')
            pm2_5 = components.get('pm2_5')
            pm10 = components.get('pm10')
            nh3 = components.get('nh3')
            dt = air_quality['dt']  # DateTime remains as string

            # Insert data into the AirQualityData table
            c.execute('''
                INSERT INTO AirQualityData 
                (city_id, co, no2, o3, so2, pm2_5, pm10, nh3, dt)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (city_id, co, no2, o3, so2, pm2_5, pm10, nh3, dt))

    conn.commit()


# Insert data from JSON file into database
insert_data_from_json('air_quality_30_6-22_9.json')

conn.close()
print("Data inserted successfully.")
