from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Database Configuration
app.config['MYSQL_HOST'] = 'localhost'  # MySQL host
app.config['MYSQL_PORT'] = 3306  # MySQL port
app.config['MYSQL_USER'] = 'root'  # MySQL username
app.config['MYSQL_PASSWORD'] = 'your_mysql_password'  # MySQL password
app.config['MYSQL_DB'] = 'your_database_name'  # MySQL database name

mysql = MySQL(app)

# Define function to help execute SQL queries
def execute_query(query, values=None):
    try:
        cursor = mysql.connection.cursor()
        if values:
            cursor.execute(query, values)
        else:
            cursor.execute(query)
        mysql.connection.commit()
        cursor.close()
        return True
    except Exception as e:
        return str(e)

# Define function to fetch data from the database
def fetch_data(query, values=None):
    try:
        cursor = mysql.connection.cursor()
        if values:
            cursor.execute(query, values)
        else:
            cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        return data
    except Exception as e:
        return str(e)

# Routes for customers table
@app.route("/customers", methods=["GET"])
def get_customers():    # Define function to get data from customers table
    try:
        query = "SELECT * FROM customers"
        params = []
        for key, value in request.args.items():
            query += f" WHERE {key} = %s"
            params.append(value)
        cursor = mysql.connection.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        customers = cursor.fetchall()
        cursor.close()
        return jsonify(customers)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Define route to get customers according to customerNumber
@app.route("/customers/<int:customer_id>", methods=["GET"])
def get_customer(customer_id): # Define function to get the information
    try:
        query = "SELECT * FROM customers WHERE customerNumber = %s"
        data = fetch_data(query, (customer_id,))
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Define function to create tables to the API
@app.route("/customers", methods=["POST"])
def add_customer():
    try:
        data = request.get_json()
        columns = ', '.join(data.keys())
        values_template = ', '.join(['%s'] * len(data.values()))
        query = f"INSERT INTO customers ({columns}) VALUES ({values_template})"
        result = execute_query(query, tuple(data.values()))
        if result:
            return jsonify({"message": "Customer added successfully"}), 201
        else:
            return jsonify({"error": "Failed to add customer"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Define route to input information for the tables created
@app.route("/customers/<int:customer_id>", methods=["PUT"])
def update_customer(customer_id):
    try:
        data = request.get_json()
        placeholders = ', '.join([f"{key} = %s" for key in data.keys()])
        values = tuple(data.values()) + (customer_id,)
        query = f"UPDATE customers SET {placeholders} WHERE customerNumber = %s"
        result = execute_query(query, values)
        if result:
            return jsonify({"message": "Customer updated successfully"})
        else:
            return jsonify({"error": "Failed to update customer"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Define route to delete customer_id
@app.route("/customers/<int:customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
    try:
        query = "DELETE FROM customers WHERE customerNumber = %s"
        result = execute_query(query, (customer_id,))
        if result:
            return jsonify({"message": "Customer deleted successfully"})
        else:
            return jsonify({"error": "Failed to delete customer"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Routes for employees table (similar structure as customers table)

# Routes for orders table (similar structure as customers table)

# Routes for order details table (similar structure as customers table)

if __name__ == "__main__":
    app.run(debug=True)

