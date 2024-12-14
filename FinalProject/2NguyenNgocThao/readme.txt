
 ERD (Entity Relationship Diagram) City và AirQualityData



 1. Bảng City  

| Field          | Type       | Description                        |
|----------------|------------|------------------------------------|
| id             | INTEGER    | Khóa chính (Primary Key)           |
| city_name      | TEXT       | Tên thành phố                      |
| latitude       | REAL       | Vĩ độ                              |
| longitude      | REAL       | Kinh độ                            |

 2. Bảng AirQualityData  

| Field          | Type       | Description                                     |
|----------------|------------|-------------------------------------------------|
| id             | INTEGER    | Khóa chính (Primary Key)                        |
| city_id        | INTEGER    | Khóa ngoại (Foreign Key) liên kết với bảng City |
| aqi            | INTEGER    | Chỉ số chất lượng không khí                     |
| co             | REAL       | Nồng độ khí CO                                  |
| no             | REAL       | Nồng độ khí NO                                  |
| no2            | REAL       | Nồng độ khí NO2                                 |
| o3             | REAL       | Nồng độ khí O3                                  |
| so2            | REAL       | Nồng độ khí SO2                                 |
| pm2_5          | REAL       | Nồng độ bụi mịn PM2.5                           |
| pm10           | REAL       | Nồng độ bụi mịn PM10                            |
| nh3            | REAL       | Nồng độ khí NH3                                 |
| dt             | TEXT       | Thời gian đo lường (timestamp)                  |

 Mối quan hệ giữa các bảng  
- 1:N (One-to-Many): Một thành phố trong bảng City có thể có nhiều bản ghi về chất lượng không khí trong bảng AirQualityData.
    - city_id trong bảng AirQualityData là khóa ngoại, liên kết đến khóa chính id trong bảng City.

 Sơ đồ ERD


                      +---------------+           +--------------------+
                      |    City       |           |  AirQualityData    |
                      +---------------+           +--------------------+
                      | id (PK)       | 1       n | id (PK)            |
                      | city_name     |<----------| city_id (FK)       |
                      | latitude      |           | aqi                |
                      | longitude     |           | co                 |
                      |               |           | no                 |
                      |               |           | no2                |
                      |               |           | o3                 |
                      |               |           | so2                |
                      |               |           | pm2_5              |
                      |               |           | pm10               |
                      |               |           | nh3                |
                      |               |           | dt                 |
                      +---------------+           +--------------------+


- Bảng City này lưu trữ các thông tin cơ bản về thành phố, chẳng hạn như tên thành phố và tọa độ địa lý.
- Bảng AirQualityData lưu các chỉ số chất lượng không khí như PM2.5, PM10, CO, NO2, SO2, O3, và thời gian đo lường cho mỗi thành phố.
- Mối quan hệ 1:N có nghĩa là một thành phố có thể có nhiều bản ghi về chất lượng không khí ở các thời điểm khác nhau.


 Luồng dữ liệu

 1. Nguồn dữ liệu (file JSON)  
Dữ liệu chất lượng không khí được thu thập từ API hoặc nguồn dữ liệu bên ngoài và được lưu trữ dưới dạng file JSON. Mỗi bản ghi trong file JSON chứa thông tin về thành phố, tọa độ địa lý, và các thông số chất lượng không khí như PM2.5, PM10, CO, NO2,...

 2. Tiền xử lý dữ liệu  
- Đọc file JSON bằng cách sử dụng thư viện json để phân tích dữ liệu.
- Mỗi bản ghi trong file JSON sẽ được trích xuất thông tin như tên thành phố, tọa độ, và thông số chất lượng không khí.

 3. Lưu trữ dữ liệu vào bảng City  
- Hệ thống kiểm tra xem thành phố trong file JSON có tồn tại trong bảng City hay chưa, dựa trên tên của thành phố:
    + Nếu đã tồn tại, hệ thống sẽ lấy city_id tương ứng.
    + Nếu chưa tồn tại, hệ thống sẽ thêm một bản ghi mới cho thành phố với các thông tin như city_name, latitude, và longitude. Sau khi chèn, city_id của thành phố mới sẽ được lấy để sử dụng cho bước tiếp theo.

 4. Lưu trữ dữ liệu vào bảng AirQualityData  
- Sau khi có city_id từ bảng City, hệ thống sẽ lưu trữ các thông số chất lượng không khí vào bảng AirQualityData.
- Các trường thông tin sẽ bao gồm: city_id, aqi (Chỉ số chất lượng không khí), co (nồng độ CO), no2 (nồng độ NO2), pm2_5, pm10, và dt (thời gian đo lường).
- Mỗi lần đo chất lượng không khí sẽ tạo ra một bản ghi mới trong bảng AirQualityData, được liên kết với city_id của thành phố tương ứng.

 5. Lưu trữ và hoàn tất  
- Sau khi dữ liệu được lưu trữ vào cả hai bảng City và AirQualityData, các thay đổi sẽ được commit vào cơ sở dữ liệu để đảm bảo rằng dữ liệu được lưu trữ vĩnh viễn.
- Kết nối cơ sở dữ liệu sẽ được đóng sau khi hoàn tất việc chèn dữ liệu.