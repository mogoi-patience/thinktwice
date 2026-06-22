from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

app = Flask(__name__)
CORS(app)

app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

mysql = MySQL(app)

@app.route('/')
def index():
    return jsonify({'message': 'ThinkTwice API is running!'})

@app.route('/api/test-db')
def test_db():
    try:
        cur = mysql.connection.cursor()
        cur.execute('SELECT 1')
        cur.close()
        return jsonify({'status': 'success', 'message': 'Database connected!'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/products', methods=['GET'])
def get_products():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM products ORDER BY created_at DESC")
        rows = cur.fetchall()
        cur.close()
        products = []
        for row in rows:
            products.append({
                'id': row[0],
                'name': row[1],
                'description': row[2],
                'price': float(row[3]),
                'stock_quantity': row[4],
                'category': row[5],
                'size': row[6],
                'image_url': row[7],
                'is_on_offer': bool(row[8]),
                'offer_price': float(row[9]) if row[9] else None,
                'created_at': str(row[10])
            })
        return jsonify({'status': 'success', 'products': products})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/products', methods=['POST'])
def add_product():
    try:
        data = request.get_json()
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO products (name, description, price, stock_quantity, category, size, image_url, is_on_offer, offer_price)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            data['name'], data.get('description'), data['price'],
            data.get('stock_quantity', 0), data.get('category'),
            data.get('size'), data.get('image_url'),
            data.get('is_on_offer', False), data.get('offer_price')
        ))
        mysql.connection.commit()
        cur.close()
        return jsonify({'status': 'success', 'message': 'Product added!'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)

@app.route('/api/subscribe', methods=['POST'])
def subscribe():
    try:
        data = request.get_json()
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO subscribers (email, phone) VALUES (%s, %s)",
                    (data['email'], data.get('phone')))
        mysql.connection.commit()
        cur.close()
        return jsonify({'status': 'success', 'message': 'Subscribed!'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
