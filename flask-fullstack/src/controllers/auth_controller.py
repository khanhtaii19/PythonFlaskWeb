import datetime
import bcrypt
import jwt
from flask import request, jsonify
from src.config.database import get_db
from src.config import JWT_SECRET, JWT_EXPIRE_DAYS, ADMIN_EMAIL, ADMIN_PASSWORD


def _normalize_email(email: str) -> str:
    return email.strip().lower()


def _hash_password(plain: str) -> str:
    return bcrypt.hashpw(plain.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def _check_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode('utf-8'), hashed.encode('utf-8'))


def _generate_token(user_id: str, email: str, role: str) -> str:
    payload = {
        'userId': user_id,
        'email':  email,
        'role':   role,
        'exp':    datetime.datetime.utcnow() + datetime.timedelta(days=JWT_EXPIRE_DAYS)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm='HS256')


# ─── POST /api/auth/register ─────────────────────────────────────────────────
def register():
    data  = request.get_json() or {}
    email = _normalize_email(data.get('email', ''))
    name  = data.get('name', '').strip()
    password = data.get('password', '')
    phone    = data.get('phone', '')

    if not email or not name or not password:
        return jsonify({'success': False, 'message': 'Missing required fields'}), 400

    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM users WHERE email = %s", (email,))
            if cur.fetchone():
                return jsonify({'success': False, 'message': 'User already exists'}), 400

            hashed = _hash_password(password)
            role   = 'admin' if email == ADMIN_EMAIL else 'user'

            cur.execute(
                """INSERT INTO users (name, email, password, phone, role)
                   VALUES (%s, %s, %s, %s, %s)""",
                (name, email, hashed, phone, role)
            )
            cur.execute("SELECT id, email, name, role FROM users WHERE email = %s", (email,))
            user = cur.fetchone()

        return jsonify({
            'success': True,
            'message': 'User registered successfully',
            'data': user
        }), 201
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        conn.close()


# ─── POST /api/auth/login ─────────────────────────────────────────────────────
def login():
    data     = request.get_json() or {}
    email    = _normalize_email(data.get('email', ''))
    password = data.get('password', '')

    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, email, name, password, role, avatar FROM users WHERE email = %s",
                (email,)
            )
            user = cur.fetchone()

        if not user:
            return jsonify({'success': False, 'message': 'Invalid credentials'}), 401

        # Admin env-password override
        if email == ADMIN_EMAIL and ADMIN_PASSWORD:
            valid = (password == ADMIN_PASSWORD)
        else:
            valid = _check_password(password, user['password'])

        if not valid:
            return jsonify({'success': False, 'message': 'Sai mat khau'}), 401

        role = 'admin' if email == ADMIN_EMAIL else user['role']

        # Promote role in DB if needed
        if role == 'admin' and user['role'] != 'admin':
            conn2 = get_db()
            try:
                with conn2.cursor() as cur2:
                    cur2.execute("UPDATE users SET role='admin' WHERE id=%s", (user['id'],))
            finally:
                conn2.close()

        token = _generate_token(user['id'], user['email'], role)

        return jsonify({
            'success': True,
            'message': 'Login successful',
            'token':   token,
            'data': {
                'id':     user['id'],
                'email':  user['email'],
                'name':   user['name'],
                'role':   role,
                'avatar': user['avatar']
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        conn.close()


# ─── GET /api/auth/me ─────────────────────────────────────────────────────────
def get_me():
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return jsonify({'success': False, 'message': 'No token provided'}), 401

    token = auth_header.split(' ')[1]
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
    except jwt.InvalidTokenError:
        return jsonify({'success': False, 'message': 'Invalid or expired token'}), 401

    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, email, name, role, avatar, phone, member_level, total_spent "
                "FROM users WHERE id = %s",
                (payload['userId'],)
            )
            user = cur.fetchone()

        if not user:
            return jsonify({'success': False, 'message': 'User not found'}), 404

        return jsonify({'success': True, 'data': user})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        conn.close()


# ─── GET /api/auth/users ──────────────────────────────────────────────────────
def get_users():
    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, name, email, phone, role, member_level, total_spent, avatar, "
                "is_active, created_at FROM users"
            )
            users = cur.fetchall()

        # Convert datetime objects to strings for JSON
        for u in users:
            if u.get('created_at'):
                u['created_at'] = str(u['created_at'])

        return jsonify({'success': True, 'data': users})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        conn.close()
