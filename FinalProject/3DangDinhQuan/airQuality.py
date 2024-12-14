import json
from datetime import datetime
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MaxNLocator

import os

def test_db_connection():
    try:
        conn = sqlite3.connect('air_quality.db')
        conn.close()
        print("Database connection successful!")
        return True
    except sqlite3.Error as e:
        print(f"Database connection failed: {e}")
        return False

if test_db_connection():
    print("Proceeding to update air_quality_data.json from the database...")
else:
    print("Unable to update data due to connection issues.")

def calculate_aqi(concentration, breakpoints):
    C_low, C_high, I_low, I_high = breakpoints
    return (I_high - I_low) / (C_high - C_low) * (concentration - C_low) + I_low

# xxx concentration 0.0-30 -> AQI 0-150
aqi_breakpoints = {
    "pm2_5": [(0.0, 12.0, 0, 50), (12.1, 35.4, 51, 100), (35.5, 55.4, 101, 150), (55.5, 150.4, 151, 200), (150.5, 250.4, 201, 300)],
    "pm10": [(0, 54, 0, 50), (55, 154, 51, 100), (155, 254, 101, 150), (255, 354, 151, 200), (355, 424, 201, 300)],
    "co": [(0.0, 4.4, 0, 50), (4.5, 9.4, 51, 100), (9.5, 12.4, 101, 150), (12.5, 15.4, 151, 200), (15.5, 30.4, 201, 300)],
    "no2": [(0.0, 53, 0, 50), (54, 100, 51, 100), (101, 360, 101, 150), (361, 649, 151, 200), (650, 1249, 201, 300)],
    "o3": [(0, 54, 0, 50), (55, 70, 51, 100), (71, 85, 101, 150), (86, 105, 151, 200), (106, 200, 201, 300)],
    "so2": [(0.0, 35, 0, 50), (36, 75, 51, 100), (76, 185, 101, 150), (186, 304, 151, 200), (305, 604, 201, 300)],
    "nh3": [(0.0, 35, 0, 200), (36, 75, 201, 400), (76, 185, 401, 800), (186, 304, 801, 1200), (305, 604, 1201, 1800)],
}

def get_aqi(concentration, pollutant):
    for bp in aqi_breakpoints[pollutant]:
        if bp[0] <= concentration <= bp[1]:
            return calculate_aqi(concentration, bp)
    return None

def get_recommendation(aqi):
    if aqi is None:
        return None
    
    if aqi <= 50:
        return {"level": "Good", "implications": "Air quality is considered satisfactory.", "recommendation": "Enjoy your outdoor activities."}
    elif aqi <= 100:
        return {"level": "Moderate", "implications": "Air quality is acceptable; however, for some pollutants, there may be a moderate health concern.", "recommendation": "Sensitive individuals should consider limiting prolonged outdoor exertion."}
    elif aqi <= 150:
        return {"level": "Unhealthy for Sensitive Groups", "implications": "Members of sensitive groups may experience health effects. The general public is not likely to be affected.", "recommendation": "Limit prolonged outdoor exertion if you are sensitive to air pollution."}
    elif aqi <= 200:
        return {"level": "Unhealthy", "implications": "Everyone may begin to experience health effects; members of sensitive groups may experience more serious health effects.", "recommendation": "Limit outdoor exertion."}
    elif aqi <= 300:
        return {"level": "Very Unhealthy", "implications": "Health alert: everyone may experience more serious health effects.", "recommendation": "Avoid all outdoor exertion."}
    else:
        return {"level": "Hazardous", "implications": "Health warnings of emergency conditions. The entire population is more likely to be affected.", "recommendation": "Remain indoors and avoid all outdoor exertion."}


#connect db and get all data
def get_all_air_quality_data():
    conn = sqlite3.connect('air_quality.db')
    c = conn.cursor()
    c.execute('''
        SELECT City.city_name, AirQualityData.dt, AirQualityData.pm2_5, AirQualityData.pm10, 
               AirQualityData.co, AirQualityData.no2, AirQualityData.so2, AirQualityData.o3, AirQualityData.nh3
        FROM AirQualityData
        JOIN City ON AirQualityData.city_id = City.id
    ''')
    
    rows = c.fetchall()
    
    data = []
    for row in rows:
        # Ensure the timestamp is in datetime format
        timestamp = pd.to_datetime(row[1], errors='coerce')  # Convert to datetime
        
        if pd.notna(timestamp):  # Only add valid timestamps
            data.append({
                "city_name": row[0],
                "timestamp": timestamp.isoformat(),  # Save as ISO format string
                "pm2_5": row[2],
                "pm10": row[3],
                "co": row[4],
                "no2": row[5],
                "so2": row[6],
                "o3": row[7],
                "nh3": row[8]
            })
    # Lưu dữ liệu mới vào file json
    json_data = json.dumps(data, indent=4)
    
    with open('air_quality_history.json', 'w') as json_file:
        json_file.write(json_data)
    print("air_quality_history.json has been updated successfully with new data from the database.")
    
    conn.close()
    
    return json_data

def process_air_quality_data(json_data):
    air_quality_data = json.loads(json_data)
    overall_aqi_list = []  # List to store overall AQI for each city
    
    for city_data in air_quality_data:
        city_name = city_data["city_name"]
        timestamp = pd.to_datetime(city_data["timestamp"], errors='coerce')  # Ensure it's a datetime
        if pd.isna(timestamp):  # Skip invalid timestamps
            continue
        
        # Get AQI values for pollutants
        pm25_aqi = get_aqi(city_data["pm2_5"], "pm2_5")
        pm10_aqi = get_aqi(city_data["pm10"], "pm10")
        co_aqi = get_aqi(city_data["co"], "co")
        no2_aqi = get_aqi(city_data["no2"], "no2")
        o3_aqi = get_aqi(city_data["o3"], "o3")
        so2_aqi = get_aqi(city_data["so2"], "so2")
        nh3_aqi = get_aqi(city_data["nh3"], "nh3")
        
        aqi_values = [pm25_aqi, pm10_aqi, co_aqi, no2_aqi, o3_aqi, so2_aqi, nh3_aqi]
        overall_aqi = max((aqi for aqi in aqi_values if aqi is not None), default=None)
        recommendation = get_recommendation(overall_aqi)

        # Append the results to overall_aqi_list
        overall_aqi_list.append({"city_name": city_name, "overall_aqi": overall_aqi, "recommendation": recommendation})

        print(f"\nCity: {city_name}")
        print(f"Timestamp (UTC): {timestamp}")
        print(f"Overall AQI: {overall_aqi}")

        if recommendation:
            print(f"Recommendation: {recommendation['recommendation']}")

    return overall_aqi_list  # Ensure this returns the complete list

def load_air_quality_json_file():
    with open('air_quality_history.json', 'r') as f:
        json_data = f.read()
    process_air_quality_data(json_data)

def load_data_from_json():
    with open('air_quality_history.json', 'r') as f:
        json_data = json.load(f)
    
    df = pd.DataFrame(json_data)
    
    # Convert the 'timestamp' column to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce') 
    
    # Calculate AQI for each pollutant and create new AQI columns
    df['pm2_5_aqi'] = df['pm2_5'].apply(lambda x: get_aqi(x, 'pm2_5') if pd.notna(x) else None)
    df['pm10_aqi'] = df['pm10'].apply(lambda x: get_aqi(x, 'pm10') if pd.notna(x) else None)
    df['co_aqi'] = df['co'].apply(lambda x: get_aqi(x, 'co') if pd.notna(x) else None)
    df['no2_aqi'] = df['no2'].apply(lambda x: get_aqi(x, 'no2') if pd.notna(x) else None)
    df['so2_aqi'] = df['so2'].apply(lambda x: get_aqi(x, 'so2') if pd.notna(x) else None)
    df['o3_aqi'] = df['o3'].apply(lambda x: get_aqi(x, 'o3') if pd.notna(x) else None)
    df['nh3_aqi'] = df['nh3'].apply(lambda x: get_aqi(x, 'nh3') if pd.notna(x) else None)
    
    # Calculate overall AQI as the maximum of the individual pollutant AQIs
    df['overall_aqi'] = df[['pm2_5_aqi', 'pm10_aqi', 'co_aqi', 'no2_aqi', 'so2_aqi', 'o3_aqi', 'nh3_aqi']].max(axis=1)
    
    return df

#Hàm này tạo và lưu các biểu đồ cho thấy nồng độ của các chất ô nhiễm khác nhau ở các thành phố khác nhau theo thời gian.

def plot_pollutants_comparison(df):
    df = df.copy()
    
    # Ensure 'timestamp' is in datetime format
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    df = df.dropna(subset=['timestamp'])  # Drop rows with NaN timestamps
    df.set_index('timestamp', inplace=True)  # Set index to timestamp
    
    pollutants = ['pm2_5', 'pm10', 'co', 'no2', 'so2', 'o3', 'nh3']  # List of pollutants to plot
    
    for pollutant in pollutants:
        plt.figure(figsize=(14, 7))
        legend_added = False
        
        for city in df['city_name'].unique():
            city_data = df[df['city_name'] == city]
            
            if city_data[pollutant].notna().any():  # Check if any data is available for the pollutant
                print(f"Plotting data for city: {city}, pollutant: {pollutant}")
                plt.plot(city_data.index, city_data[pollutant], marker='o', label=city)
                legend_added = True  # Set to True if data was plotted
        
        # Set plot title and labels
        plt.title(f'{pollutant.upper()} Levels Across Cities')
        plt.xlabel('Date')
        plt.ylabel(f'{pollutant.upper()} Concentration (µg/m³ or ppm)')
        plt.xticks(rotation=45)
        plt.gca().xaxis.set_major_locator(MaxNLocator(nbins=10))
        plt.grid()
        plt.legend()
            
        #     # Save the plot instead of showing it
        output_folder = 'city_plots'
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        plt.savefig(f'{output_folder}/{pollutant}_comparison.png')
        
        plt.close()  # Close the figure after saving

def plot_overall_aqi(overall_aqi_list):
    df = pd.DataFrame(overall_aqi_list)

    if df.empty:
        print("No AQI data available for plotting.")
        return

    # Check if 'overall_aqi' column exists
    if 'overall_aqi' not in df.columns:
        print("Column 'overall_aqi' does not exist in the DataFrame.")
        return
    
    # Calculate average AQI for each city
    avg_aqi = df.groupby('city_name')['overall_aqi'].mean().reset_index()

    plt.figure(figsize=(10, 6))

    # Define color mapping based on AQI ranges
    def get_color(aqi):
        if aqi <= 50:
            return 'green'        # Good
        elif aqi <= 100:
            return 'yellow'       # Moderate
        elif aqi <= 150:
            return 'orange'       # Unhealthy for Sensitive Groups
        elif aqi <= 200:
            return 'red'          # Unhealthy
        elif aqi <= 300:
            return 'purple'       # Very Unhealthy
        else:
            return 'darkred'      # Hazardous

    # Create bars with colors based on AQI
    bars = plt.bar(avg_aqi['city_name'], avg_aqi['overall_aqi'], 
                   color=[get_color(aqi) for aqi in avg_aqi['overall_aqi']])
    
    # Annotate each bar with its height (AQI value)
    for bar in bars:
        yval = bar.get_height()  # Get the height of the bar (AQI value)
        plt.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 2), 
                 ha='center', va='bottom', fontsize=10)  # Add text at the top of the bar

    plt.title('Average Overall AQI per City')
    plt.xlabel('City')
    plt.ylabel('Average Overall AQI')
    plt.xticks(rotation=45)
    plt.ylim(0, 300)  # Adjust according to your AQI scale
    plt.tight_layout()

    # Adding an explanation box
    explanation_text = (
        "AQI Levels:\n"
        "0-50: Good\n"
        "51-100: Moderate\n"
        "101-150: Unhealthy for Sensitive Groups\n"
        "151-200: Unhealthy\n"
        "201-300: Very Unhealthy\n"
        "301+: Hazardous"
    )
    
    plt.gcf().text(0.6999, 0.75, explanation_text, fontsize=10, bbox=dict(facecolor='white', alpha=0.5))
    # Save the plot as a PNG file
    plt.savefig('city_plots/average_aqi_per_city.png')
    plt.close()


def visualize_comparisons(filtered_df):
    plot_pollutants_comparison(filtered_df)
    # plot_overall_aqi(df)  # Add this line to plot overall AQI
    if 'overall_aqi' in filtered_df.columns:
        overall_aqi_list = filtered_df[['city_name', 'overall_aqi']].dropna().to_dict('records')
        plot_overall_aqi(overall_aqi_list)
    else:
        print("'overall_aqi' column not found for plotting AQI comparison.")
    
    print("Pollutant comparison plots have been generated for all cities and saved to the 'city_plots' folder.")


def check_data(df):
    print("Checking data...")
    print(df.head())  # Check if the data has been loaded correctly
    print(df.info())  # Check for NaN values and data types
# Function to filter data based on the date range
def filter_data_within_date_range(df, user_start_date, user_end_date):
    # Convert user input to pd.Timestamp
    user_start_date = pd.to_datetime(user_start_date, errors='coerce')
    user_end_date = pd.to_datetime(user_end_date, errors='coerce')
    
    # Check for valid dates
    if pd.isna(user_start_date) or pd.isna(user_end_date):
        raise ValueError("Invalid date provided. Please enter dates in the correct format (YYYY-MM-DD).")

    # Filter the DataFrame
    filtered_df = df[(df['timestamp'] >= user_start_date) & (df['timestamp'] <= user_end_date)]

     # Check if 'overall_aqi' is in the filtered DataFrame
    if 'overall_aqi' not in filtered_df.columns:
        print("Column 'overall_aqi' does not exist in the filtered DataFrame.")
    
    return filtered_df
json_data = get_all_air_quality_data()  
df = load_data_from_json() 
overall_aqi_list = process_air_quality_data(json_data)
check_data(df)  

user_start_date = input("Enter a start date between 2024-07-01 and 2024-09-24: ")
user_end_date = input("Enter an end date between 2024-07-01 and 2024-09-24: ")
try:
    filtered_df = filter_data_within_date_range(df, user_start_date, user_end_date)
    visualize_comparisons(filtered_df)
except ValueError as ve:
    print(ve)
except Exception as e:
    print(f"An error occurred: {e}")
plot_overall_aqi(overall_aqi_list)