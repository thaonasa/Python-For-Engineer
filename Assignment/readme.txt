
ERD (Entity Relationship Diagram) City và AirQualityData

 1. Bảng City

|  Field         | Type         | Description                            |
|----------------|--------------|----------------------------------------|
| id             | INTEGER      | Khóa chính (Primary Key)               |
| city_name      | TEXT         | Tên thành phố                          |
| latitude       | REAL         | Vĩ độ                                  |
| longitude      | REAL         | Kinh độ                                |

 2. Bảng AirQualityData

|  Field         | Type         | Description                                            |
|----------------|--------------|--------------------------------------------------------|
| id             | INTEGER      | Khóa chính (Primary Key)                               |
| city_id        | INTEGER      | Khóa ngoại (Foreign Key) liên kết với bảng City        |
| co             | REAL         | Nồng độ khí CO                                         |
| no2            | REAL         | Nồng độ khí NO2                                        |
| o3             | REAL         | Nồng độ khí O3                                         |
| so2            | REAL         | Nồng độ khí SO2                                        |
| pm2_5          | REAL         | Nồng độ bụi mịn PM2.5                                  |
| pm10           | REAL         | Nồng độ bụi mịn PM10                                   |
| nh3            | REAL         | Nồng độ khí NH3                                        |
| dt             | TEXT         | Thời gian đo lường (timestamp)                         |

 Mối quan hệ giữa các bảng  
- 1:N (One-to-Many): Một thành phố trong bảng City có thể có nhiều bản ghi về chất lượng không khí trong bảng AirQualityData.
    + Trường city_id trong bảng AirQualityData là khóa ngoại, liên kết đến khóa chính id trong bảng City.

 Sơ đồ ERD


                      +---------------+           +---------------------+
                      |    City       |           |  AirQualityData     |
                      +---------------+           +---------------------+
                      | id (PK)       | 1       N | id (PK)             |
                      | city_name     |<----------| city_id (FK)        |
                      | latitude      |           | co                  |
                      | longitude     |           | no2                 |
                      +---------------+           | o3                  |
                                                  | so2                 |
                                                  | pm2_5               |
                                                  | pm10                |
                                                  | nh3                 |
                                                  | dt                  |
                                                  +---------------------+

- Bảng City lưu trữ các thông tin cơ bản về thành phố như tên thành phố và tọa độ địa lý.
- Bảng AirQualityData lưu các chỉ số chất lượng không khí như PM2.5, PM10, CO, NO2, SO2, O3 
và thời gian đo lường cho từng thành phố.
- Mối quan hệ 1:N nghĩa là một thành phố có thể có nhiều bản ghi về chất lượng không khí 
tại các thời điểm khác nhau.

 Luồng dữ liệu

1. Nguồn dữ liệu (file JSON)  
   Dữ liệu chất lượng không khí được thu thập từ API hoặc nguồn dữ liệu bên ngoài và lưu trữ dưới dạng file JSON. 
   Mỗi bản ghi trong file chứa thông tin về thành phố, tọa độ địa lý và các chỉ số chất lượng không khí như:
   PM2.5, PM10, CO, NO2,...

2. Tiền xử lý dữ liệu
   - Đọc file JSON bằng thư viện json để phân tích dữ liệu.
   - Mỗi bản ghi sẽ được trích xuất các thông tin như tên thành phố, tọa độ, và chỉ số chất lượng không khí.

3. Lưu trữ dữ liệu vào bảng City
   - Kiểm tra xem thành phố có tồn tại trong bảng City chưa:
     - Nếu tồn tại, lấy city_id tương ứng.
     - Nếu chưa tồn tại, thêm một bản ghi mới cho thành phố với các thông tin như city_name, latitude, và longitude. Sau khi thêm, city_id của thành phố mới sẽ được lấy để sử dụng cho bước tiếp theo.

4. Lưu trữ dữ liệu vào bảng AirQualityData
   - Sau khi có city_id, các chỉ số chất lượng không khí sẽ được lưu vào bảng AirQualityData.
   - Các trường lưu trữ bao gồm: city_id, co, no2, pm2_5, pm10, dt (thời gian đo lường).
   - Mỗi lần đo lường sẽ tạo ra một bản ghi mới trong bảng AirQualityData, 
   liên kết với city_id của thành phố tương ứng.

5. Lưu trữ và hoàn tất
   - Sau khi dữ liệu được lưu vào cả hai bảng City và AirQualityData,
   hệ thống sẽ commit thay đổi để đảm bảo dữ liệu được lưu trữ vĩnh viễn.
   - Đóng kết nối cơ sở dữ liệu sau khi hoàn tất việc lưu trữ.

--------------------------------------------------------------------------------------------------------------------

 ERD (Entity Relationship Diagram) City and AirQualityData

 1. City Table

| Field          | Data Type   | Description                         |
|----------------|-------------|-------------------------------------|
| id             | INTEGER     | Primary Key                         |
| city_name      | TEXT        | City name                           |
| latitude       | REAL        | Latitude                            |
| longitude      | REAL        | Longitude                           |

 2. AirQualityData Table

| Field          | Data Type   | Description                                            |
|----------------|-------------|--------------------------------------------------------|
| id             | INTEGER     | Primary Key                                            |
| city_id        | INTEGER     | Foreign Key linking to the City table                  |
| co             | REAL        | CO concentration                                       |
| no2            | REAL        | NO2 concentration                                      |
| o3             | REAL        | O3 concentration                                       |
| so2            | REAL        | SO2 concentration                                      |
| pm2_5          | REAL        | PM2.5 concentration                                    |
| pm10           | REAL        | PM10 concentration                                     |
| nh3            | REAL        | NH3 concentration                                      |
| dt             | TEXT        | Measurement timestamp                                  |

 Relationship between Tables  
- 1:N (One-to-Many): A city in the City table can have many air quality records in the AirQualityData table.
    + The city_id field in the AirQualityData table is a foreign key linking to the primary key id in the City table.

 ERD Diagram


                      +---------------+           +--------------------+
                      |    City       |           |  AirQualityData    |
                      +---------------+           +--------------------+
                      | id (PK)       | 1       N | id (PK)            |
                      | city_name     |<----------| city_id (FK)       |
                      | latitude      |           | co                 |
                      | longitude     |           | no2                |
                      +---------------+           | o3                 |
                                                  | so2                |
                                                  | pm2_5              |
                                                  | pm10               |
                                                  | nh3                |
                                                  | dt                 |
                                                  +--------------------+


 Explanation:

- City Table stores basic information about a city, such as the city name and its geographical coordinates.
- AirQualityData Table stores air quality indices like PM2.5, PM10, CO, NO2, SO2, O3, and the measurement time for each city.
- The 1:N relationship means that one city can have multiple air quality records at different times.

 Data Flow

1. Data Source (JSON file)  
   Air quality data is collected from an API or external data source and stored as a JSON file. Each record in the file contains information about the city, geographical coordinates, and air quality parameters such as PM2.5, PM10, CO, NO2,...

2. Data Preprocessing
   - Read the JSON file using the json library to parse the data.
   - Each record in the file will be extracted to retrieve information such as city name, coordinates, and air quality parameters.

3. Store Data in the City Table
   - The system checks if the city exists in the City table based on the city name:
     - If it exists, the corresponding city_id is retrieved.
     - If not, a new record is added for the city with information like city_name, latitude, and longitude. After insertion, the city_id of the new city is retrieved for use in the next step.

4. Store Data in the AirQualityData Table
   - After obtaining the city_id from the City table, the air quality parameters are stored in the AirQualityData table.
   - The fields include: city_id, co, no2, pm2_5, pm10, and dt (measurement timestamp).
   - Each air quality measurement creates a new record in the AirQualityData table, linked to the city_id of the corresponding city.

5. Store and Finalize
   - Once the data has been stored in both the City and AirQualityData tables, the changes are committed to the database to ensure the data is saved permanently.
   - The database connection is closed after the data insertion process is complete.