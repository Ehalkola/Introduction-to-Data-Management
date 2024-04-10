from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import mysql.connector

#
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:B33t4s4lp44j42023@localhost/mybusiness'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['passwd'] = 'B33t4s4lp44j42023'
db = SQLAlchemy(app)

# Define classess for customer, salesman and order table in mysql

class Customer(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True)
    cust_name = db.Column(db.String(100))
    city = db.Column(db.String(100))
    grade = db.Column(db.String(10))
    salesman_id = db.Column(db.Integer)
    def __repr__(self):
        return f"<Customer {self.customer_id}: {self.cust_name} ({self.city})>"

class Salesman(db.Model):
    salesman_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    city = db.Column(db.String(100))
    commission = db.Column(db.Float)
    def __repr__(self):
        return f"<Salesman {self.id}: {self.name} ({self.city})>"

class Order(db.Model):
    ord_no = db.Column(db.Integer, primary_key=True)
    purch_amt = db.Column(db.Float)
    ord_date = db.Column(db.Date)  # Added ord_date column
    customer_id = db.Column(db.Integer)
    salesman_id = db.Column(db.Integer)
    __tablename__ = 'orders'  # Specify table name
    def __repr__(self):
        return f"<Order {self.ord_no}: Purchased Amount: {self.purch_amt}, Date: {self.ord_date}>"

# Get all customers 
@app.route('/customers', methods=['GET'])
def get_all_customers():
    try:
        customers = Customer.query.all()
        data = [{'customer_id': customer.customer_id, 'cust_name': customer.cust_name, 'city': customer.city,
                 'grade': customer.grade, 'salesman_id': customer.salesman_id} for customer in customers]
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Get customer by ID
@app.route('/customers/<int:customer_id>', methods=['GET'])
def get_customer_by_id(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    return jsonify({'customer_id': customer.customer_id, 'cust_name': customer.cust_name, 'city': customer.city,
                    'grade': customer.grade, 'salesman_id': customer.salesman_id})

# Add a new customer
@app.route('/customers', methods=['POST'])
def add_customer():
    try:
        data = request.json
        customer = Customer(cust_name=data['cust_name'], city=data['city'],
                            grade=data['grade'], salesman_id=data['salesman_id'])
        db.session.add(customer)
        db.session.commit()
        return f'Customer added successfully!', 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Update a customer by ID
@app.route('/customers/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    try:
        data = request.json
        customer = Customer.query.get_or_404(customer_id)
        
        if 'cust_name' in data:
            customer.cust_name = data['cust_name']
        if 'city' in data:
            customer.city = data['city']
        if 'grade' in data:
            customer.grade = data['grade']
        if 'salesman_id' in data:
            customer.salesman_id = data['salesman_id']
        
        db.session.commit()
        return f'Customer information replaced, , customer_id {customer_id}.', 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Patch a customer by ID
@app.route('/customers/<int:customer_id>', methods=['PATCH'])
def patch_customer(customer_id):
    try:
        data = request.json
        customer = Customer.query.get_or_404(customer_id)
        
        for key, value in data.items():
            setattr(customer, key, value)
        
        db.session.commit()
        return f'Customer updated, customer_id {customer_id}.', 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Delete a customer by ID
@app.route('/customers/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    try:
        customer = Customer.query.get_or_404(customer_id)
        db.session.delete(customer)
        db.session.commit()
        return f'Customer deleted, customer_id {customer_id}.', 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Get all salesmen
@app.route('/salesmen', methods=['GET'])
def get_all_salesmen():
    try:
        salesmen = Salesman.query.all()
        data = [{'salesman_id': salesman.salesman_id, 'name': salesman.name, 'city': salesman.city,
                 'commission': salesman.commission} for salesman in salesmen]
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Get salesman by ID
@app.route('/salesmen/<int:salesman_id>', methods=['GET'])
def get_salesman_by_id(salesman_id):
    salesman = Salesman.query.get_or_404(salesman_id)
    return jsonify({'salesman_id': salesman.salesman_id, 'name': salesman.name, 'city': salesman.city,
                    'commission': salesman.commission})

# Add a new salesman
@app.route('/salesmen', methods=['POST'])
def add_salesman():
    try:
        data = request.json
        salesman = Salesman(name=data['name'], city=data['city'],
                            commission=data['commission'])
        db.session.add(salesman)
        db.session.commit()
        return 'Salesman added successfully!', 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Update a salesman by ID
@app.route('/salesmen/<int:salesman_id>', methods=['PUT'])
def replace_salesman(salesman_id):
    try:
        data = request.json
        salesman = Salesman.query.get_or_404(salesman_id)
        
        if 'name' in data:
            salesman.name = data['name']
        if 'city' in data:
            salesman.city = data['city']
        if 'commission' in data:
            salesman.commission = data['commission']
        
        db.session.commit()
        return f'Salesman information replaced, salesman_id {salesman_id}.', 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Patch a salesman by ID
@app.route('/salesmen/<int:salesman_id>', methods=['PATCH'])
def patch_salesman(salesman_id):
    try:
        data = request.json
        salesman = Salesman.query.get_or_404(salesman_id)
        
        for key, value in data.items():
            setattr(salesman, key, value)
        
        db.session.commit()
        return f'Salesman patched, salesman_id {salesman_id}.', 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Delete a salesman by ID
@app.route('/salesmen/<int:salesman_id>', methods=['DELETE'])
def delete_salesman(salesman_id):
    try:
        salesman = Salesman.query.get_or_404(salesman_id)
        db.session.delete(salesman)
        db.session.commit()
        return f'Salesman deleted, salesman_id {salesman_id}.', 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Get all orders
@app.route('/orders', methods=['GET'])
def get_all_orders():
    try:
        orders = Order.query.all()
        data = [{'ord_no': order.ord_no, 'purch_amt': order.purch_amt,
                 'ord_date': order.ord_date.strftime('%Y-%m-%d'),
                 'customer_id': order.customer_id, 'salesman_id': order.salesman_id} for order in orders]
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Get order by ord_no
@app.route('/orders/<int:ord_no>', methods=['GET'])
def get_order_by_ord_no(ord_no):
    order = Order.query.get_or_404(ord_no)
    return jsonify({'ord_no': order.ord_no, 'purch_amt': order.purch_amt,
                    'ord_date': order.ord_date.strftime('%Y-%m-%d'),
                    'customer_id': order.customer_id, 'salesman_id': order.salesman_id})

# Add a new order
@app.route('/orders', methods=['POST'])
def add_order():
    try:
        data = request.json
        order = Order(ord_no=data['ord_no'], purch_amt=data['purch_amt'],
                      ord_date=datetime.strptime(data['ord_date'], '%Y-%m-%d').date(),
                      customer_id=data['customer_id'], salesman_id=data['salesman_id'])
        db.session.add(order)
        db.session.commit()
        return 'Order added successfully!', 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Update an order by ord_no
@app.route('/orders/<int:ord_no>', methods=['PUT'])
def update_order(ord_no):
    try:
        data = request.json
        order = Order.query.get_or_404(ord_no)
        order.purch_amt = data['purch_amt']
        order.ord_date = datetime.strptime(data['ord_date'], '%Y-%m-%d').date()
        order.customer_id = data['customer_id']
        order.salesman_id = data['salesman_id']
        db.session.commit()
        return f'Order information replaced, ord_no {ord_no}.', 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Patch an order by ord_no
@app.route('/orders/<int:ord_no>', methods=['PATCH'])
def patch_order(ord_no):
    try:
        data = request.json
        order = Order.query.get_or_404(ord_no)
        for key, value in data.items():
            setattr(order, key, value)
        db.session.commit()
        return f'Order updated, ord_no {ord_no}.', 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Delete an order by ord_no
@app.route('/orders/<int:ord_no>', methods=['DELETE'])
def delete_order(ord_no):
    try:
        order = Order.query.get_or_404(ord_no)
        db.session.delete(order)
        db.session.commit()
        return f'Order deleted, ord_no {ord_no}.', 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Run the app/file
if __name__ == '__main__':
    app.run(debug=True)
