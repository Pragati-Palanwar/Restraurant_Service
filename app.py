from flask import Flask, request, jsonify, render_template
import sqlite3
from flask_cors import CORS

app = Flask(__name__,  static_url_path='/static')
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

def dict_from_row(row):
    return dict(zip(row.keys(), row))

def get_db_connection():
    conn = sqlite3.connect('restaurant.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/products', methods=['GET'])
def get_products():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products')
    products = [dict_from_row(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(products)

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products WHERE id=?', (product_id,))
    product = dict_from_row(cursor.fetchone())
    conn.close()
    if product:
        return jsonify(product)
    else:
        return jsonify({'error': 'Product not found'}), 404


@app.route('/products', methods=['POST'])
def create_product():
    conn = get_db_connection()
    cursor = conn.cursor()
    data = request.json
    name = data['name']
    price = data['price']
    description = data.get('description', '')

    cursor.execute('INSERT INTO products (name, price, description) VALUES (?, ?, ?)', (name, price, description))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Product created successfully'}), 201


@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    data = request.json
    name = data['name']
    price = data['price']
    description = data.get('description', '')

    cursor.execute('UPDATE products SET name=?, price=?, description=? WHERE id=?', (name, price, description, product_id))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Product updated successfully'})


@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM products WHERE id=?', (product_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Product deleted successfully'})


@app.route('/orders', methods=['POST'])
def place_order():
    conn = get_db_connection()
    cursor = conn.cursor()
    data = request.json
    product_id = data['product_id']
    quantity = data['quantity']

    cursor.execute('SELECT * FROM products WHERE id=?', (product_id,))
    product = cursor.fetchone()
    if product:
        cursor.execute('INSERT INTO orders (product_id, quantity) VALUES (?, ?)', (product_id, quantity))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Order placed successfully'}), 201
    else:
        return jsonify({'error': 'Product not found'}), 404


@app.route('/orders', methods=['GET'])
def list_orders():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM orders')
    orders = [dict_from_row(row) for row in cursor.fetchall()]
    
    conn.close()
    return jsonify(orders)

@app.route('/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM orders WHERE id=?', (order_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Order Delievered'})



if __name__ == '__main__':
    app.run(debug=True)
