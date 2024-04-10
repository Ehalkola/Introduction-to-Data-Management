from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

# Initialize your MySQL database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:B33t4s4lp44j42023@localhost/mybusiness'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the Order class
class Order(db.Model):
    ord_no = db.Column(db.Integer, primary_key=True)
    purch_amt = db.Column(db.Float)
    ord_date = db.Column(db.Date)
    customer_id = db.Column(db.Integer)
    salesman_id = db.Column(db.Integer)
    __tablename__ = 'orders'

# Define the OrderDetails class
class OrderDetails:
    def get_orders_with_aggregation(self, agg_type=None):
        if agg_type is None:
            orders = Order.query.all()
            data = [{'ord_no': order.ord_no, 'purch_amt': order.purch_amt,
                     'ord_date': order.ord_date.strftime('%Y-%m-%d'),
                     'customer_id': order.customer_id, 'salesman_id': order.salesman_id} for order in orders]
            return jsonify(data)
        
        query = db.session.query(Order)
        if agg_type == 'sum':
            total = db.session.query(func.sum(Order.purch_amt)).scalar()
            return jsonify({'Total purch amount of all orders:': total})
        elif agg_type == 'avg':
            average = db.session.query(func.avg(Order.purch_amt)).scalar()
            return jsonify({'Average purchase amount:': average})
        elif agg_type == 'count':
            count = db.session.query(func.count(Order.ord_no)).scalar()
            return jsonify({'Total order amount:': count})
        else:
            return jsonify({'error': 'Invalid aggregation type. Valid types are: sum, avg, count, None'}), 400

@app.route('/orderdetails', methods=['GET'])
def get_order_details_with_aggregation():
    agg_type = request.args.get('aggregate')
    order_details = OrderDetails()
    return order_details.get_orders_with_aggregation(agg_type)

# Get all order details for a specific orderNumber
@app.route('/orderdetails/<int:order_no>', methods=['GET'])
def get_order_details_by_order_no(order_no):
    try:
        # Fetch all order details based on order_no
        order_details = Order.query.filter_by(ord_no=order_no).all()
        
        if order_details:
            # If order details are found, format them into a list of dictionaries
            data = [{
                'ord_no': order_detail.ord_no,
                'purch_amt': order_detail.purch_amt,
                'ord_date': order_detail.ord_date.strftime('%Y-%m-%d'),
                'customer_id': order_detail.customer_id,
                'salesman_id': order_detail.salesman_id
            } for order_detail in order_details]
        else:
            # If no order details are found, set data to an empty list
            data = []
            
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Route for adding a new order
@app.route('/orderdetails', methods=['POST'])
def add_order():
    # Get order data from the request JSON
    data = request.get_json()
    
    # Create a new Order instance
    new_order = Order(
        ord_no=data['ord_no'],
        purch_amt=data['purch_amt'],
        ord_date=data['ord_date'],
        customer_id=data['customer_id'],
        salesman_id=data['salesman_id']
    )

    # Add the new order to the database session and commit
    db.session.add(new_order)
    db.session.commit()

    # Return a success message
    return jsonify({'message': 'New order added successfully'}), 201

# Route for updating an existing order
@app.route('/orderdetails/<int:ord_no>', methods=['PATCH'])
def update_order(ord_no):
    # Get the updated order data from the request JSON
    data = request.get_json()
    
    # Retrieve the order to be updated from the database
    order = Order.query.get(ord_no)
    
    # Update the order fields with the new values
    if order:
        for key, value in data.items():
            setattr(order, key, value)
        
        # Commit the changes to the database
        db.session.commit()
        
        return jsonify({'message': f'Order {ord_no} updated successfully'}), 200
    else:
        return jsonify({'error': f'Order {ord_no} not found'}), 404
    
# Route for deleting an existing order
@app.route('/orderdetails/<int:ord_no>', methods=['DELETE'])
def delete_order(ord_no):
    # Retrieve the order to be deleted from the database
    order = Order.query.get(ord_no)
    
    # Delete the order if found
    if order:
        db.session.delete(order)
        db.session.commit()
        return jsonify({'message': f'Order {ord_no} deleted successfully'}), 200
    else:
        return jsonify({'error': f'Order {ord_no} not found'}), 404

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
