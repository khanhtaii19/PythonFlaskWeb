import json
from flask import request, jsonify
from src.config.database import get_db


def _serialize(row: dict) -> dict:
    for k, v in row.items():
        if hasattr(v, 'isoformat'):
            row[k] = str(v)
        elif hasattr(v, '__float__'):
            row[k] = float(v)
    return row


def _build_order_response(order: dict, items: list) -> dict:
    """
    Reconstruct the frontend-friendly Order shape from DB rows.
    The frontend stores customerInfo inside `notes` as JSON.
    """
    notes_raw = order.get('notes') or '{}'
    try:
        notes_obj = json.loads(notes_raw)
    except (json.JSONDecodeError, TypeError):
        notes_obj = {}

    customer_info = notes_obj.get('customerInfo', {
        'name': '', 'phone': '', 'email': '',
        'province': '', 'district': '', 'ward': '', 'addressDetail': ''
    })
    original_payment = notes_obj.get('originalPaymentMethod', order.get('payment_method', 'cod'))

    # Rebuild CartItem-like structure for each order item
    cart_items = []
    for item in items:
        cart_items.append({
            'product': {
                'id':          item['product_id'],
                'name':        item.get('product_name', ''),
                'description': item.get('product_description', ''),
                'image':       item.get('product_image', ''),
                'price':       float(item.get('product_price', 0)),
                'salePrice':   float(item.get('product_sale_price')) if item.get('product_sale_price') else None,
                'stock':       item.get('product_stock', 0),
                'categoryId':  item.get('product_category_id', ''),
                'details':     item.get('product_details', ''),
            },
            'quantity': item['quantity']
        })

    return {
        'id':              order['id'],
        'userId':          order['user_id'],
        'items':           cart_items,
        'totalAmount':     float(order['total_amount']),
        'discountAmount':  float(order.get('discount_amount', 0)),
        'finalAmount':     float(order['final_amount']),
        'couponCode':      order.get('coupon_code'),
        'status':          order['status'],
        'paymentMethod':   original_payment,
        'customerInfo':    customer_info,
        'createdAt':       str(order['created_at']),
    }


# ─── GET /api/orders ──────────────────────────────────────────────────────────
def get_orders():
    user_id = request.args.get('userId')
    conn = get_db()
    try:
        with conn.cursor() as cur:
            if user_id:
                cur.execute("SELECT * FROM orders WHERE user_id = %s ORDER BY created_at DESC", (user_id,))
            else:
                cur.execute("SELECT * FROM orders ORDER BY created_at DESC")
            orders = cur.fetchall()

            result = []
            for order in orders:
                cur.execute(
                    """SELECT oi.*, p.name AS product_name, p.description AS product_description,
                              p.image AS product_image, p.price AS product_price,
                              p.sale_price AS product_sale_price, p.stock AS product_stock,
                              p.category_id AS product_category_id, p.details AS product_details
                       FROM order_items oi
                       LEFT JOIN products p ON oi.product_id = p.id
                       WHERE oi.order_id = %s""",
                    (order['id'],)
                )
                items = cur.fetchall()
                result.append(_build_order_response(order, items))

        return jsonify({'success': True, 'data': result})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        conn.close()


# ─── POST /api/orders ─────────────────────────────────────────────────────────
def create_order():
    data = request.get_json() or {}
    conn = get_db()
    try:
        with conn.cursor() as cur:
            shipping = data.get('shippingAddress', {})
            cur.execute(
                """INSERT INTO orders
                   (user_id, total_amount, discount_amount, final_amount,
                    coupon_code, status, payment_method,
                    street, city, state, zip_code, country, notes)
                   VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                (
                    data.get('userId', 'guest'),
                    data.get('totalAmount', 0),
                    data.get('discountAmount', 0),
                    data.get('finalAmount', data.get('totalAmount', 0)),
                    data.get('couponCode'),
                    data.get('status', 'pending'),
                    data.get('paymentMethod', 'cash'),
                    shipping.get('street', ''),
                    shipping.get('city', ''),
                    shipping.get('state', ''),
                    shipping.get('zipCode', ''),
                    shipping.get('country', 'Vietnam'),
                    data.get('notes', '{}')
                )
            )
            # Get the inserted order id (UUID-based, fetch latest by user+time)
            cur.execute(
                "SELECT id FROM orders WHERE user_id = %s ORDER BY created_at DESC LIMIT 1",
                (data.get('userId', 'guest'),)
            )
            order_row = cur.fetchone()
            order_id  = order_row['id']

            # Insert order items
            for item in data.get('items', []):
                cur.execute(
                    "INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (%s,%s,%s,%s)",
                    (order_id, item['productId'], item['quantity'], item['price'])
                )

            cur.execute("SELECT * FROM orders WHERE id = %s", (order_id,))
            order = cur.fetchone()
            cur.execute(
                """SELECT oi.*, p.name AS product_name, p.description AS product_description,
                          p.image AS product_image, p.price AS product_price,
                          p.sale_price AS product_sale_price, p.stock AS product_stock,
                          p.category_id AS product_category_id, p.details AS product_details
                   FROM order_items oi
                   LEFT JOIN products p ON oi.product_id = p.id
                   WHERE oi.order_id = %s""",
                (order_id,)
            )
            items = cur.fetchall()

        return jsonify({
            'success': True,
            'data': _build_order_response(order, items),
            'message': 'Order created successfully'
        }), 201
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400
    finally:
        conn.close()


# ─── PUT /api/orders/<id>/status ─────────────────────────────────────────────
def update_order_status(order_id):
    data   = request.get_json() or {}
    status = data.get('status')
    if not status:
        return jsonify({'success': False, 'message': 'Status is required'}), 400

    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM orders WHERE id = %s", (order_id,))
            if not cur.fetchone():
                return jsonify({'success': False, 'message': 'Order not found'}), 404

            cur.execute("UPDATE orders SET status = %s WHERE id = %s", (status, order_id))
            cur.execute("SELECT * FROM orders WHERE id = %s", (order_id,))
            order = cur.fetchone()
            cur.execute(
                """SELECT oi.*, p.name AS product_name, p.description AS product_description,
                          p.image AS product_image, p.price AS product_price,
                          p.sale_price AS product_sale_price, p.stock AS product_stock,
                          p.category_id AS product_category_id, p.details AS product_details
                   FROM order_items oi
                   LEFT JOIN products p ON oi.product_id = p.id
                   WHERE oi.order_id = %s""",
                (order_id,)
            )
            items = cur.fetchall()

        return jsonify({
            'success': True,
            'data': _build_order_response(order, items),
            'message': 'Order status updated successfully'
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400
    finally:
        conn.close()
