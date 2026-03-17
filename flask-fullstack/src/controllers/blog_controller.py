import json
from flask import request, jsonify
from src.config.database import get_db


def _serialize_post(row: dict) -> dict:
    for k, v in row.items():
        if hasattr(v, 'isoformat'):
            row[k] = str(v)

    # Parse JSON columns
    if isinstance(row.get('content'), str):
        try:
            row['content'] = json.loads(row['content'])
        except Exception:
            row['content'] = [row['content']]

    if isinstance(row.get('tags'), str):
        try:
            row['tags'] = json.loads(row['tags'])
        except Exception:
            row['tags'] = []

    # Reshape author sub-object
    row['author'] = {
        'name':     row.pop('author_name', ''),
        'avatar':   row.pop('author_avatar', ''),
        'readTime': row.pop('author_read_time', ''),
        'date':     row.get('post_date', ''),
    }

    # Rename post_date → date for frontend compatibility
    if 'post_date' in row:
        row['date'] = row.pop('post_date')

    return row


# ─── GET /api/blog ────────────────────────────────────────────────────────────
def get_blog_posts():
    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM blog_posts ORDER BY post_date DESC")
            rows = [_serialize_post(r) for r in cur.fetchall()]
        return jsonify({'success': True, 'data': rows})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        conn.close()


# ─── GET /api/blog/<id> ───────────────────────────────────────────────────────
def get_blog_post_by_id(post_id):
    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM blog_posts WHERE id = %s", (post_id,))
            row = cur.fetchone()
        if not row:
            return jsonify({'success': False, 'message': 'Blog post not found'}), 404
        return jsonify({'success': True, 'data': _serialize_post(row)})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        conn.close()


# ─── POST /api/blog ───────────────────────────────────────────────────────────
def create_blog_post():
    data   = request.get_json() or {}
    author = data.get('author', {})
    conn   = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """INSERT INTO blog_posts
                   (title, excerpt, content, post_date, category, image,
                    author_name, author_avatar, author_read_time, tags)
                   VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                (
                    data.get('title'),
                    data.get('excerpt'),
                    json.dumps(data.get('content', []), ensure_ascii=False),
                    data.get('date'),
                    data.get('category'),
                    data.get('image'),
                    author.get('name', ''),
                    author.get('avatar', ''),
                    author.get('readTime', ''),
                    json.dumps(data.get('tags', []), ensure_ascii=False),
                )
            )
            cur.execute("SELECT * FROM blog_posts ORDER BY created_at DESC LIMIT 1")
            row = cur.fetchone()
        return jsonify({
            'success': True,
            'data': _serialize_post(row),
            'message': 'Blog post created successfully'
        }), 201
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400
    finally:
        conn.close()
