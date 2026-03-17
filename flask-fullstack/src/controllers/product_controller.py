from flask import request, jsonify
from src.config.database import get_db


def _serialize(row: dict) -> dict:
    """Convert datetime/Decimal to JSON-safe types."""
    for k, v in row.items():
        if hasattr(v, 'isoformat'):
            row[k] = str(v)
        elif hasattr(v, '__float__'):
            row[k] = float(v)
    return row


# ─── GET /api/products ────────────────────────────────────────────────────────
def get_products():
    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM products ORDER BY created_at DESC")
            rows = [_serialize(r) for r in cur.fetchall()]
        return jsonify({'success': True, 'data': rows})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        conn.close()


# ─── GET /api/products/<id> ───────────────────────────────────────────────────
def get_product_by_id(product_id):
    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM products WHERE id = %s", (product_id,))
            row = cur.fetchone()
        if not row:
            return jsonify({'success': False, 'message': 'Product not found'}), 404
        return jsonify({'success': True, 'data': _serialize(row)})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        conn.close()


# ─── POST /api/products ───────────────────────────────────────────────────────
def create_product():
    data = request.get_json() or {}
    required = ['name', 'description', 'details', 'price', 'costPrice', 'stock', 'image', 'categoryId']
    for field in required:
        if field not in data:
            return jsonify({'success': False, 'message': f'Missing field: {field}'}), 400

    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """INSERT INTO products
                   (category_id, name, description, details, price, sale_price,
                    cost_price, stock, total_sold, image, promotion_text)
                   VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                (
                    data.get('categoryId'),
                    data.get('name'),
                    data.get('description'),
                    data.get('details'),
                    data.get('price'),
                    data.get('salePrice'),
                    data.get('costPrice', 0),
                    data.get('stock', 0),
                    data.get('totalSold', 0),
                    data.get('image'),
                    data.get('promotionText')
                )
            )
            cur.execute("SELECT * FROM products WHERE id = LAST_INSERT_ID()")
            # LAST_INSERT_ID doesn't work with UUID; use separate query
            cur.execute(
                "SELECT * FROM products ORDER BY created_at DESC LIMIT 1"
            )
            row = cur.fetchone()
        return jsonify({'success': True, 'data': _serialize(row), 'message': 'Product created successfully'}), 201
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400
    finally:
        conn.close()


# ─── PUT /api/products/<id> ───────────────────────────────────────────────────
def update_product(product_id):
    data = request.get_json() or {}
    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM products WHERE id = %s", (product_id,))
            if not cur.fetchone():
                return jsonify({'success': False, 'message': 'Product not found'}), 404

            fields = {
                'category_id':    data.get('categoryId'),
                'name':           data.get('name'),
                'description':    data.get('description'),
                'details':        data.get('details'),
                'price':          data.get('price'),
                'sale_price':     data.get('salePrice'),
                'cost_price':     data.get('costPrice'),
                'stock':          data.get('stock'),
                'total_sold':     data.get('totalSold'),
                'image':          data.get('image'),
                'promotion_text': data.get('promotionText'),
            }
            # Only update provided fields
            updates = {k: v for k, v in fields.items() if v is not None}
            if updates:
                set_clause = ', '.join(f"`{k}` = %s" for k in updates)
                values = list(updates.values()) + [product_id]
                cur.execute(f"UPDATE products SET {set_clause} WHERE id = %s", values)

            cur.execute("SELECT * FROM products WHERE id = %s", (product_id,))
            row = cur.fetchone()
        return jsonify({'success': True, 'data': _serialize(row), 'message': 'Product updated successfully'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400
    finally:
        conn.close()


# ─── DELETE /api/products/<id> ────────────────────────────────────────────────
def delete_product(product_id):
    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM products WHERE id = %s", (product_id,))
            if not cur.fetchone():
                return jsonify({'success': False, 'message': 'Product not found'}), 404
            cur.execute("DELETE FROM products WHERE id = %s", (product_id,))
        return jsonify({'success': True, 'message': 'Product deleted successfully'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        conn.close()
