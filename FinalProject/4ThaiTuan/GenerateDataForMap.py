import sqlite3
import json

# Hàm tính toán AQI dựa trên các ngưỡng chất ô nhiễm
def calculate_aqi(concentration, breakpoints):
    C_low, C_high, I_low, I_high = breakpoints
    return (I_high - I_low) / (C_high - C_low) * (concentration - C_low) + I_low

# Ngưỡng AQI cho các chất ô nhiễm
aqi_breakpoints = {
    "pm2_5": [(0.0, 12.0, 0, 50), (12.1, 35.4, 51, 100), (35.5, 55.4, 101, 150), (55.5, 150.4, 151, 200), (150.5, 250.4, 201, 300)],
    "pm10": [(0, 54, 0, 50), (55, 154, 51, 100), (155, 254, 101, 150), (255, 354, 151, 200), (355, 424, 201, 300)],
    "co": [(0.0, 4.4, 0, 50), (4.5, 9.4, 51, 100), (9.5, 12.4, 101, 150), (12.5, 15.4, 151, 200), (15.5, 30.4, 201, 300)],
    "no2": [(0.0, 53, 0, 50), (54, 100, 51, 100), (101, 360, 101, 150), (361, 649, 151, 200), (650, 1249, 201, 300)],
    "o3": [(0, 54, 0, 50), (55, 70, 51, 100), (71, 85, 101, 150), (86, 105, 151, 200), (106, 200, 201, 300)],
    "so2": [(0.0, 35, 0, 50), (36, 75, 51, 100), (76, 185, 101, 150), (186, 304, 151, 200), (305, 604, 201, 300)],
    "nh3": [(0.0, 35, 0, 200), (36, 75, 201, 400), (76, 185, 401, 800), (186, 304, 801, 1200), (305, 604, 1201, 1800)]
}

# Hàm lấy AQI dựa trên nồng độ chất ô nhiễm
def get_aqi(concentration, pollutant):
    if pollutant in aqi_breakpoints:
        for bp in aqi_breakpoints[pollutant]:
            if bp[0] <= concentration <= bp[1]:
                return calculate_aqi(concentration, bp)
    return None

aqi_recommendations = [
    {"range": (0, 50), "level": "Good", "implications": "Air quality is good.", "recommendation": "No action needed."},
    {"range": (51, 100), "level": "Moderate", "implications": "Some pollutants may affect sensitive groups.", "recommendation": "Limit outdoor activities."},
    {"range": (101, 150), "level": "Unhealthy for Sensitive Groups", "implications": "Sensitive groups may experience health effects.", "recommendation": "Reduce prolonged outdoor exertion."},
    {"range": (151, 200), "level": "Unhealthy", "implications": "Everyone may experience health effects; sensitive groups may experience more serious health effects.", "recommendation": "Limit outdoor activities."},
    {"range": (201, 300), "level": "Very Unhealthy", "implications": "Health alert: everyone may experience more serious health effects.", "recommendation": "Avoid all outdoor activities."},
    {"range": (301, 500), "level": "Hazardous", "implications": "Health warning of emergency conditions.", "recommendation": "Stay indoors; avoid all outdoor exertion."},
]

def get_recommendation(overall_aqi):
    for recommendation in aqi_recommendations:
        if recommendation["range"][0] <= overall_aqi <= recommendation["range"][1]:
            return recommendation
    return None

# Hàm tính AQI tổng thể từ các chất ô nhiễm
def calculate_overall_aqi(components):
    aqi_values = []
    for pollutant, concentration in components.items():
        if concentration is not None:
            concentration = round(concentration, 1)  # Làm tròn giá trị nồng độ
        aqi = get_aqi(concentration, pollutant)
        if aqi is not None:
            aqi_values.append(aqi)
    
    if aqi_values:
        return max(aqi_values)  # Chọn AQI lớn nhất
    return None

# Kết nối đến SQLite và lấy dữ liệu
def load_air_quality_from_db(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    query = '''
    SELECT City.city_name, City.latitude, City.longitude, AirQualityData.dt, 
               AirQualityData.pm2_5, AirQualityData.pm10, 
               AirQualityData.co, AirQualityData.no2, AirQualityData.so2, AirQualityData.o3, AirQualityData.nh3
        FROM AirQualityData
        JOIN City ON AirQualityData.city_id = City.id
    '''
    cursor.execute(query)
    rows = cursor.fetchall()

    data = {}

    for row in rows:
        city = row[0]
        coordinates = [round(row[1], 4), round(row[2], 4)]  # Làm tròn tọa độ cho nhỏ gọn
        timestamp = row[3]
        components = {
            "pm2_5": row[4],
            "pm10": row[5],
            "co": row[6],
            "no2": row[7],
            "so2": row[8],
            "o3": row[9],
            "nh3": row[10]
        }

        overall_aqi = calculate_overall_aqi(components)
        recommendation = get_recommendation(overall_aqi)

        if city not in data:
            data[city] = {
                "name": city,
                "coordinates": coordinates,
                "data": []
            }

        data[city]["data"].append({
            "timestamp": timestamp,
            "aqi": round(overall_aqi, 1) if overall_aqi else None,
            "pm2_5": round(components["pm2_5"], 1) if components["pm2_5"] else None,
            "pm10": round(components["pm10"], 1) if components["pm10"] else None,
            "co": round(components["co"], 1) if components["co"] else None,
            "no2": round(components["no2"], 1) if components["no2"] else None,
            "so2": round(components["so2"], 1) if components["so2"] else None,
            "o3": round(components["o3"], 1) if components["o3"] else None,
            "nh3": round(components["nh3"], 1) if components["nh3"] else None,
            "recommendation": recommendation['recommendation'] if recommendation else None
        })

    conn.close()
    return list(data.values())

# Xuất dữ liệu ra file JSON với định dạng minify (loại bỏ khoảng trắng)
def save_to_json(data, output_file):
    with open(output_file, 'w') as f:
        json.dump(data, f, separators=(',', ':'))  # Minify JSON

# Đường dẫn tới file cơ sở dữ liệu SQLite và file JSON đầu ra
db_path = 'air_quality_30_6-22_9.db'
output_json = './html/air_quality_output_minified.json'

# Load dữ liệu từ SQLite và lưu ra JSON
air_quality_data = load_air_quality_from_db(db_path)
save_to_json(air_quality_data, output_json)

print(f"Dữ liệu đã được lưu vào {output_json}")
