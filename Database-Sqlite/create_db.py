import sqlite3

# Kết nối tới cơ sở dữ liệu
conn = sqlite3.connect('sales_management.db')
cursor = conn.cursor()

# Tạo bảng Customers
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Customers (
        customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT NOT NULL,
        phone TEXT
    )
''')

# Tạo bảng Products
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products (
        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_name TEXT NOT NULL,
        price REAL NOT NULL
    )
''')

# Tạo bảng Orders
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Orders (
        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER,
        order_date TEXT NOT NULL,
        FOREIGN KEY (customer_id) REFERENCES Customers (customer_id)
    )
''')

# Tạo bảng OrderDetails
cursor.execute('''
    CREATE TABLE IF NOT EXISTS OrderDetails (
        order_id INTEGER,
        product_id INTEGER,
        quantity INTEGER NOT NULL,
        PRIMARY KEY (order_id, product_id),
        FOREIGN KEY (order_id) REFERENCES Orders (order_id),
        FOREIGN KEY (product_id) REFERENCES Products (product_id)
    )
''')

# Xác nhận thay đổi và đóng kết nối
conn.commit()
conn.close()

