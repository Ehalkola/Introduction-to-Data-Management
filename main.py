from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:B33t4s4lp44j42023@localhost/mybusiness'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['passwd'] = 'B33t4s4lp44j42023'
db = SQLAlchemy(app)

class Customer(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True)
    cust_name = db.Column(db.String(100))
    city = db.Column(db.String(100))
    grade = db.Column(db.String(10))
    salesman_id = db.Column(db.Integer)

    def __repr__(self):
        return f"<Customer {self.customer_id}: {self.cust_name} ({self.city})>"

class Salesman(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    city = db.Column(db.String(100))
    commission = db.Column(db.Float)

    def __repr__(self):
        return f"<Salesman {self.id}: {self.name} ({self.city})>"

class Ord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ord_no = db.Column(db.Integer)
    purch_amt = db.Column(db.Float)
    customer_id = db.Column(db.Integer)

    def __repr__(self):
        return f"<Ord {self.id}: Order No. {self.ord_no}, Purchased Amount: {self.purch_amt}>"


@app.route('/customers', methods=['GET'])
def get_customers():
    cust_name = request.args.get('cust_name')
    city = request.args.get('city')
    grade = request.args.get('grade')
    salesman_id = request.args.get('salesman_id')
    try:
        query = Customer.query
        if cust_name:
            query = query.filter_by(cust_name=cust_name)
        if city:
            query = query.filter_by(city=city)
        if grade:
            query = query.filter_by(grade=grade)
        if salesman_id:
            query = query.filter_by(salesman_id=salesman_id)
        customers = query.all()
        data = [{'customer_id': customer.customer_id, 'cust_name': customer.cust_name, 'city': customer.city,
                 'grade': customer.grade, 'salesman_id': customer.salesman_id} for customer in customers]
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/customers/<int:customer_id>', methods=['GET', 'PUT', 'DELETE'])
def customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    if request.method == 'GET':
        return jsonify({'customer_id': customer.customer_id, 'cust_name': customer.cust_name, 'city': customer.city,
                        'grade': customer.grade, 'salesman_id': customer.salesman_id})
    elif request.method == 'PUT':
        try:
            data = request.json
            customer.cust_name = data.get('cust_name', customer.cust_name)
            customer.city = data.get('city', customer.city)
            customer.grade = data.get('grade', customer.grade)
            customer.salesman_id = data.get('salesman_id', customer.salesman_id)
            db.session.commit()
            return 'Customer updated', 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    elif request.method == 'DELETE':
        try:
            db.session.delete(customer)
            db.session.commit()
            return 'Customer deleted', 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    else:
        return 'Invalid request', 400

@app.route('/customers', methods=['POST'])
def add_customer():
    try:
        data = request.json
        customer = Customer(cust_name=data['cust_name'], city=data['city'],
                            grade=data['grade'], salesman_id=data['salesman_id'])
        db.session.add(customer)
        db.session.commit()
        return 'Customer added', 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/salesmen', methods=['GET'])
def get_salesmen():
    try:
        salesmen = Salesman.query.all()
        data = [{'id': salesman.id, 'name': salesman.name, 'city': salesman.city,
                 'commission': salesman.commission} for salesman in salesmen]
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/salesmen/<int:salesman_id>', methods=['GET', 'PUT', 'DELETE'])
def salesman(salesman_id):
    salesman = Salesman.query.get_or_404(salesman_id)

    if request.method == 'GET':
        return jsonify({'id': salesman.id, 'name': salesman.name, 'city': salesman.city,
                        'commission': salesman.commission})
    elif request.method == 'PUT':
        try:
            data = request.json
            salesman.name = data.get('name', salesman.name)
            salesman.city = data.get('city', salesman.city)
            salesman.commission = data.get('commission', salesman.commission)
            db.session.commit()
            return 'Salesman updated', 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    elif request.method == 'DELETE':
        try:
            db.session.delete(salesman)
            db.session.commit()
            return 'Salesman deleted', 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    else:
        return 'Invalid request', 400
    
    
@app.route('/salesmen', methods=['POST'])
def add_salesman():
    try:
        data = request.json
        salesman = Salesman(name=data['name'], city=data['city'],
                            commission=data['commission'])
        db.session.add(salesman)
        db.session.commit()
        return 'Salesman added', 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/ords', methods=['GET'])
def get_orders():
    try:
        orders = Ord.query.all()
        data = [{'id': order.id, 'ord_no': order.ord_no, 'purch_amt': order.purch_amt,
                 'customer_id': order.customer_id} for order in orders]
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/ords/<int:ord_id>', methods=['GET', 'PUT', 'DELETE'])
def order(ord_id):
    order = Ord.query.get_or_404(ord_id)
    if request.method == 'GET':
        return jsonify({'id': order.id, 'ord_no': order.ord_no, 'purch_amt': order.purch_amt,
                        'customer_id': order.customer_id})
    elif request.method == 'PUT':
        try:
            data = request.json
            order.ord_no = data.get('ord_no', order.ord_no)
            order.purch_amt = data.get('purch_amt', order.purch_amt)
            order.customer_id = data.get('customer_id', order.customer_id)
            db.session.commit()
            return 'Order updated', 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    elif request.method == 'DELETE':
        try:
            db.session.delete(order)
            db.session.commit()
            return 'Order deleted', 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    else:
        return 'Invalid request', 400

@app.route('/ords', methods=['POST'])
def add_order():
    try:
        data = request.json
        order = Ord(ord_no=data['ord_no'], purch_amt=data['purch_amt'],
                    customer_id=data['customer_id'])
        db.session.add(order)
        db.session.commit()
        return 'Order added', 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    
    
if __name__ == '__main__':
    app.run(debug=True)
    
    
    
