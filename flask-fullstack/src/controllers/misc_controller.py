from flask import jsonify
from src.config.database import get_db


# ─── GET /api/categories ──────────────────────────────────────────────────────
def get_categories():
    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM categories ORDER BY created_at ASC")
            rows = cur.fetchall()
        for r in rows:
            for k, v in r.items():
                if hasattr(v, 'isoformat'):
                    r[k] = str(v)
        return jsonify({'success': True, 'data': rows})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        conn.close()


# ─── GET /api/coupons ─────────────────────────────────────────────────────────
def get_coupons():
    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM coupons WHERE is_active = 1")
            rows = cur.fetchall()
        for r in rows:
            for k, v in r.items():
                if hasattr(v, 'isoformat'):
                    r[k] = str(v)
        return jsonify({'success': True, 'data': rows})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        conn.close()
