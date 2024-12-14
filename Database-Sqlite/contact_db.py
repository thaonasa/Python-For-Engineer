import sqlite3


def add_customer_example():
    conn = sqlite3.connect('sales_management.db')
    cursor = conn.cursor()

    # Thêm một khách hàng
    cursor.execute('''
        INSERT INTO Customers (first_name, last_name, email, phone)
        VALUES ('Nguyen', 'Anh', 'nguyen.anh@example.com', '0123456789')
    ''')

    conn.commit()
    conn.close()


def add_order_example():
    conn = sqlite3.connect('sales_management.db')
    cursor = conn.cursor()

    # Thêm đơn hàng cho khách hàng có ID là 1
    cursor.execute('''
        INSERT INTO Orders (customer_id, order_date)
        VALUES (1, '2024-09-18')
    ''')

    conn.commit()
    conn.close()


def add_order_details_example():
    conn = sqlite3.connect('sales_management.db')
    cursor = conn.cursor()

    # Thêm chi tiết sản phẩm cho đơn hàng có order_id = 1
    order_details = [
        (1, 1, 2),  # 2 cái Bàn
        (1, 2, 4)   # 4 cái Ghế
    ]

    cursor.executemany('''
        INSERT INTO OrderDetails (order_id, product_id, quantity)
        VALUES (?, ?, ?)
    ''', order_details)

    conn.commit()
    conn.close()


def add_products_example():
    conn = sqlite3.connect('sales_management.db')
    cursor = conn.cursor()

    # Thêm 3 sản phẩm
    products = [
        ('Bàn', 1000.0),
        ('Ghế', 500.0),
        ('Đèn', 200.0)
    ]

    cursor.executemany('''
        INSERT INTO Products (product_name, price)
        VALUES (?, ?)
    ''', products)

    conn.commit()
    conn.close()


def delete_customer(customer_id):
    conn = sqlite3.connect('sales_management.db')
    cursor = conn.cursor()

    cursor.execute('''
        DELETE FROM Customers
        WHERE customer_id = ?
    ''', (customer_id,))

    conn.commit()
    conn.close()


def delete_order_product(order_id, product_id):
    conn = sqlite3.connect('sales_management.db')
    cursor = conn.cursor()

    cursor.execute('''
        DELETE FROM OrderDetails
        WHERE order_id = ? AND product_id = ?
    ''', (order_id, product_id))

    conn.commit()
    conn.close()


def get_all_customers():
    conn = sqlite3.connect('sales_management.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM Customers')
    customers = cursor.fetchall()

    conn.close()
    return customers


def get_all_orders_with_details():
    conn = sqlite3.connect('sales_management.db')
    cursor = conn.cursor()

    query = '''
        SELECT Orders.order_id, Orders.order_date, Customers.first_name, Customers.last_name, Products.product_name, OrderDetails.quantity
        FROM Orders
        JOIN Customers ON Orders.customer_id = Customers.customer_id
        JOIN OrderDetails ON Orders.order_id = OrderDetails.order_id
        JOIN Products ON OrderDetails.product_id = Products.product_id
    '''

    cursor.execute(query)
    orders = cursor.fetchall()

    conn.close()
    return orders


def get_customer_orders(customer_id):
    conn = sqlite3.connect('sales_management.db')
    cursor = conn.cursor()

    query = '''
        SELECT Orders.order_id, Orders.order_date, Products.product_name, OrderDetails.quantity
        FROM Orders
        JOIN OrderDetails ON Orders.order_id = OrderDetails.order_id
        JOIN Products ON OrderDetails.product_id = Products.product_id
        WHERE Orders.customer_id = ?
    '''

    cursor.execute(query, (customer_id,))
    orders = cursor.fetchall()

    conn.close()
    return orders


def update_order_quantity(order_id, product_id, new_quantity):
    conn = sqlite3.connect('sales_management.db')
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE OrderDetails
        SET quantity = ?
        WHERE order_id = ? AND product_id = ?
    ''', (new_quantity, order_id, product_id))

    conn.commit()
    conn.close()


def update_product_price(product_id, new_price):
    conn = sqlite3.connect('sales_management.db')
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE Products
        SET price = ?
        WHERE product_id = ?
    ''', (new_price, product_id))

    conn.commit()
    conn.close()
