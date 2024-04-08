from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)

# MySQL Configuration
conn = mysql.connector.connect(
    host='localhost',
    user='root',  # Replace with your MySQL username
    password='B33t4s4lp44j42023',  # Replace with your MySQL password
    database='mybusiness'  # Replace with your database name
)
cur = conn.cursor()

# Customers Table API Routes

# a. /customers - GET
@app.route('/customers', methods=['GET'])
def get_customers():
    try:
        query = "SELECT * FROM customers"
        cur.execute(query)
        customers = cur.fetchall()
        return jsonify(customers)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# b. /customers/<int: customer_id> - GET
@app.route('/customers/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    try:
        query = "SELECT * FROM customers WHERE customerNumber = %s"
        cur.execute(query, (customer_id,))
        customer = cur.fetchone()
        return jsonify(customer)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# c. /customers - POST
@app.route('/customers', methods=['POST'])
def add_customer():
    try:
        data = request.get_json()
        query = "INSERT INTO customers (customerName, contactLastName, contactFirstName, phone, addressLine1, addressLine2, city, state, postalCode, country, salesRepEmployeeNumber, creditLimit) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (data['customerName'], data['contactLastName'], data['contactFirstName'], data['phone'], data['addressLine1'], data['addressLine2'], data['city'], data['state'], data['postalCode'], data['country'], data['salesRepEmployeeNumber'], data['creditLimit'])
        cur.execute(query, values)
        conn.commit()
        return jsonify({"message": "Customer added successfully"}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# d. /customers/<int: customer_id> - PUT
@app.route('/customers/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    try:
        data = request.get_json()
        query = "UPDATE customers SET customerName = %s, contactLastName = %s, contactFirstName = %s, phone = %s, addressLine1 = %s, addressLine2 = %s, city = %s, state = %s, postalCode = %s, country = %s, salesRepEmployeeNumber = %s, creditLimit = %s WHERE customerNumber = %s"
        values = (data['customerName'], data['contactLastName'], data['contactFirstName'], data['phone'], data['addressLine1'], data['addressLine2'], data['city'], data['state'], data['postalCode'], data['country'], data['salesRepEmployeeNumber'], data['creditLimit'], customer_id)
        cur.execute(query, values)
        conn.commit()
        return jsonify({"message": "Customer updated successfully"})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# e. /customers/<int: customer_id> - PATCH
@app.route('/customers/<int:customer_id>', methods=['PATCH'])
def partial_update_customer(customer_id):
    try:
        data = request.get_json()
        updates = ', '.join([f"{key} = '{value}'" for key, value in data.items()])
        query = f"UPDATE customers SET {updates} WHERE customerNumber = {customer_id}"
        cur.execute(query)
        conn.commit()
        return jsonify({"message": "Customer updated successfully"})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# f. /customers/<int: customer_id> - DELETE
@app.route('/customers/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    try:
        query = "DELETE FROM customers WHERE customerNumber = %s"
        cur.execute(query, (customer_id,))
        conn.commit()
        return jsonify({"message": "Customer deleted successfully"})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Salesmen Table API Routes

# a. /salesmen - GET
@app.route('/salesmen', methods=['GET'])
def get_salesmen():
    try:
        query = "SELECT * FROM employees"
        cur.execute(query)
        salesmen = cur.fetchall()
        return jsonify(salesmen)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# b. /salesmen/<int: salesman_id> - GET
@app.route('/salesmen/<int:salesman_id>', methods=['GET'])
def get_salesman(salesman_id):
    try:
        query = "SELECT * FROM employees WHERE employeeNumber = %s"
        cur.execute(query, (salesman_id,))
        salesman = cur.fetchone()
        return jsonify(salesman)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# c. /salesmen - POST
@app.route('/salesmen', methods=['POST'])
def add_salesman():
    try:
        data = request.get_json()
        query = "INSERT INTO employees (lastName, firstName, extension, email, officeCode, reportsTo, jobTitle) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (data['lastName'], data['firstName'], data['extension'], data['email'], data['officeCode'], data['reportsTo'], data['jobTitle'])
        cur.execute(query, values)
        conn.commit()
        return jsonify({"message": "Salesman added successfully"}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# d. /salesmen/<int: salesman_id> - PUT
@app.route('/salesmen/<int:salesman_id>', methods=['PUT'])
def update_salesman(salesman_id):
    try:
        data = request.get_json()
        query = "UPDATE employees SET lastName = %s, firstName = %s, extension = %s, email = %s, officeCode = %s, reportsTo = %s, jobTitle = %s WHERE employeeNumber = %s"
        values = (data['lastName'], data['firstName'], data['extension'], data['email'], data['officeCode'], data['reportsTo'], data['jobTitle'], salesman_id)
        cur.execute(query, values)
        conn.commit()
        return jsonify({"message": "Salesman updated successfully"})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# e. /salesmen/<int: salesman_id> - PATCH
@app.route('/salesmen/<int:salesman_id>', methods=['PATCH'])
def partial_update_salesman(salesman_id):
    try:
        data = request.get_json()
        updates = ', '.join([f"{key} = '{value}'" for key, value in data.items()])
        query = f"UPDATE employees SET {updates} WHERE employeeNumber = {salesman_id}"
        cur.execute(query)
        conn.commit()
        return jsonify({"message": "Salesman updated successfully"})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# f. /salesmen/<int: salesman_id> - DELETE
@app.route('/salesmen/<int:salesman_id>', methods=['DELETE'])
def delete_salesman(salesman_id):
    try:
        query = "DELETE FROM employees WHERE employeeNumber = %s"
        cur.execute(query, (salesman_id,))
        conn.commit()
        return jsonify({"message": "Salesman deleted successfully"})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Orders Table API Routes

# a. /orders - GET
@app.route('/orders', methods=['GET'])
def get_orders():
    try:
        query = "SELECT * FROM orders"
        cur.execute(query)
        orders = cur.fetchall()
        return jsonify(orders)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# b. /orders/<int: order_id> - GET
@app.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    try:
        query = "SELECT * FROM orders WHERE orderNumber = %s"
        cur.execute(query, (order_id,))
        order = cur.fetchone()
        return jsonify(order)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# c. /orders - POST
@app.route('/orders', methods=['POST'])
def add_order():
    try:
        data = request.get_json()
        query = "INSERT INTO orders (orderDate, requiredDate, shippedDate, status, comments, customerNumber) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (data['orderDate'], data['requiredDate'], data['shippedDate'], data['status'], data['comments'], data['customerNumber'])
        cur.execute(query, values)
        conn.commit()
        return jsonify({"message": "Order added successfully"}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# d. /orders/<int: order_id> - PATCH
@app.route('/orders/<int:order_id>', methods=['PATCH'])
def update_order(order_id):
    try:
        data = request.get_json()
        query = "UPDATE orders SET orderDate = %s, requiredDate = %s, shippedDate = %s, status = %s, comments = %s, customerNumber = %s WHERE orderNumber = %s"
        values = (data['orderDate'], data['requiredDate'], data['shippedDate'], data['status'], data['comments'], data['customerNumber'], order_id)
        cur.execute(query, values)
        conn.commit()
        return jsonify({"message": "Order updated successfully"})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# e. /orders/<int: order_id> - DELETE
@app.route('/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    try:
        query = "DELETE FROM orders WHERE orderNumber = %s"
        cur.execute(query, (order_id,))
        conn.commit()
        return jsonify({"message": "Order deleted successfully"})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Orderdetails Table API Routes

# a. /orderdetails - GET
@app.route('/orderdetails', methods=['GET'])
def get_orderdetails():
    try:
        query = "SELECT * FROM orderdetails"
        cur.execute(query)
        orderdetails = cur.fetchall()
        return jsonify(orderdetails)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# b. /orderdetails/<int: order_id>/product/<product_code> - GET
@app.route('/orderdetails/<int:order_id>/product/<product_code>', methods=['GET'])
def get_orderdetail(order_id, product_code):
    try:
        query = "SELECT * FROM orderdetails WHERE orderNumber = %s AND productCode = %s"
        cur.execute(query, (order_id, product_code))
        orderdetail = cur.fetchone()
        return jsonify(orderdetail)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# c. /orderdetails - POST
@app.route('/orderdetails', methods=['POST'])
def add_orderdetail():
    try:
        data = request.get_json()
        query = "INSERT INTO orderdetails (orderNumber, productCode, quantityOrdered, priceEach, orderLineNumber) VALUES (%s, %s, %s, %s, %s)"
        values = (data['orderNumber'], data['productCode'], data['quantityOrdered'], data['priceEach'], data['orderLineNumber'])
        cur.execute(query, values)
        conn.commit()
        return jsonify({"message": "Order detail added successfully"}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# d. /orderdetails/<int: order_id>/product/<product_code> - PATCH
@app.route('/orderdetails/<int:order_id>/product/<product_code>', methods=['PATCH'])
def update_orderdetail(order_id, product_code):
    try:
        data = request.get_json()
        query = "UPDATE orderdetails SET quantityOrdered = %s, priceEach = %s, orderLineNumber = %s WHERE orderNumber = %s AND productCode = %s"
        values = (data['quantityOrdered'], data['priceEach'], data['orderLineNumber'], order_id, product_code)
        cur.execute(query, values)
        conn.commit()
        return jsonify({"message": "Order detail updated successfully"})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# e. /orderdetails/<int: order_id>/product/<product_code> - DELETE
@app.route('/orderdetails/<int:order_id>/product/<product_code>', methods=['DELETE'])
def delete_orderdetail(order_id, product_code):
    try:
        query = "DELETE FROM orderdetails WHERE orderNumber = %s AND productCode = %s"
        cur.execute(query, (order_id, product_code))
        conn.commit()
        return jsonify({"message": "Order detail deleted successfully"})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)


