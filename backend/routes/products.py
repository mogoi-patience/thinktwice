from flask import Blueprint, jsonify, request
from flask_mysqldb import MySQL

products_bp = Blueprint('products', __name__)

def init_products(mysql):

    @products_bp.route('/api/products', methods=['GET'])
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

    @products_bp.route('/api/products/<int:id>', methods=['GET'])
    def get_product(id):
        try:
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM products WHERE id = %s", (id,))
            row = cur.fetchone()
            cur.close()
            if not row:
                return jsonify({'status': 'error', 'message': 'Product not found'}), 404
            product = {
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
            }
            return jsonify({'status': 'success', 'product': product})
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500

    @products_bp.route('/api/products', methods=['POST'])
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

    @products_bp.route('/api/products/<int:id>', methods=['PUT'])
    def update_product(id):
        try:
            data = request.get_json()
            cur = mysql.connection.cursor()
            cur.execute("""
                UPDATE products SET name=%s, description=%s, price=%s,
                stock_quantity=%s, category=%s, size=%s, image_url=%s,
                is_on_offer=%s, offer_price=%s WHERE id=%s
            """, (
                data['name'], data.get('description'), data['price'],
                data.get('stock_quantity', 0), data.get('category'),
                data.get('size'), data.get('image_url'),
                data.get('is_on_offer', False), data.get('offer_price'), id
            ))
            mysql.connection.commit()
            cur.close()
            return jsonify({'status': 'success', 'message': 'Product updated!'})
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500

    @products_bp.route('/api/products/<int:id>', methods=['DELETE'])
    def delete_product(id):
        try:
            cur = mysql.connection.cursor()
            cur.execute("DELETE FROM products WHERE id = %s", (id,))
            mysql.connection.commit()
            cur.close()
            return jsonify({'status': 'success', 'message': 'Product deleted!'})
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500

    return products_bp
