"""
Seed MySQL database with sample data.
Run: python seed.py
"""
import json
import bcrypt
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from dotenv import load_dotenv
load_dotenv()

from src.config.database import get_db, init_db


def seed():
    print("🌱 Starting database seed...")
    init_db()

    conn = get_db()
    try:
        with conn.cursor() as cur:
            # ── Clear existing data ──────────────────────────────
            cur.execute("SET FOREIGN_KEY_CHECKS = 0")
            for table in ['order_items', 'orders', 'blog_posts', 'coupons', 'products', 'categories', 'users']:
                cur.execute(f"DELETE FROM `{table}`")
            cur.execute("SET FOREIGN_KEY_CHECKS = 1")
            print("🧹 Cleared existing data")

            # ── Users ────────────────────────────────────────────
            hashed = bcrypt.hashpw(b'123456', bcrypt.gensalt()).decode('utf-8')
            users = [
                ('Nguyễn Văn A', 'vana@example.com', hashed, '0901234567', 'user', 'Diamond', 15000000, 'https://i.pravatar.cc/150?u=u1'),
                ('Trần Thị B',   'thib@example.com', hashed, '0912345678', 'user', 'Gold',    5500000,  'https://i.pravatar.cc/150?u=u2'),
                ('Quản Trị Viên','admin@shop.com',   hashed, None,         'admin','Diamond',  0,        'https://i.pravatar.cc/150?u=admin'),
            ]
            cur.executemany(
                """INSERT INTO users (name, email, password, phone, role, member_level, total_spent, avatar)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                users
            )
            print(f"✅ Seeded {len(users)} users")

            # ── Categories ───────────────────────────────────────
            categories = [
                ('Món Chính',   'Các món ăn no nê, đậm đà hương vị truyền thống và hiện đại.', 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?q=80&w=2080&auto=format&fit=crop'),
                ('Khai Vị',     'Bắt đầu bữa tiệc với những món nhẹ nhàng, kích thích vị giác.', 'https://images.unsplash.com/photo-1541529086526-db283c563270?q=80&w=2070&auto=format&fit=crop'),
                ('Tráng Miệng', 'Kết thúc ngọt ngào với các loại bánh và kem đặc sắc.', 'https://images.unsplash.com/photo-1563805042-7684c019e1cb?q=80&w=1944&auto=format&fit=crop'),
            ]
            cur.executemany(
                "INSERT INTO categories (name, description, image) VALUES (%s, %s, %s)",
                categories
            )
            cur.execute("SELECT id, name FROM categories")
            cat_rows   = cur.fetchall()
            cat_map    = {r['name']: r['id'] for r in cat_rows}
            print(f"✅ Seeded {len(categories)} categories")

            # ── Products ─────────────────────────────────────────
            products = [
                (cat_map['Món Chính'],   'Pizza Hải Sản Pesto',    'Sự kết hợp hoàn hảo giữa tôm, mực tươi và sốt pesto xanh mướt.', 'Được làm từ bột tươi ủ 24h, nướng trong lò gạch truyền thống.', 220000, 185000, 120000, 50, 124, 'https://images.unsplash.com/photo-1513104890138-7c749659a591?q=80&w=2070&auto=format&fit=crop', 'Giảm giá 15% cho thành viên mới'),
                (cat_map['Món Chính'],   'Steak Thăn Nội Bò Mỹ',  'Thịt thăn mềm tan, phục vụ kèm khoai tây nghiền và sốt vang đỏ.', 'Thịt bò Black Angus được chọn lọc kỹ lưỡng.', 450000, None, 280000, 20, 45,  'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?q=80&w=2080&auto=format&fit=crop', 'Tặng 1 ly vang đỏ kèm theo'),
                (cat_map['Tráng Miệng'], 'Tiramisu Cổ Điển',       'Hương vị cà phê nồng nàn quyện cùng lớp kem béo ngậy.', 'Bánh được làm theo công thức truyền thống từ vùng Treviso.', 85000, 75000, 40000, 15, 210, 'https://images.unsplash.com/photo-1571877227200-a0d98ea607e9?q=80&w=1974&auto=format&fit=crop', None),
            ]
            cur.executemany(
                """INSERT INTO products
                   (category_id, name, description, details, price, sale_price, cost_price, stock, total_sold, image, promotion_text)
                   VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                products
            )
            print(f"✅ Seeded {len(products)} products")

            # ── Coupons ──────────────────────────────────────────
            coupons = [
                ('HELLO2026', 10, 100, 5,  '2026-12-31'),
                ('WELCOME50', 50, 50,  0,  '2026-06-30'),
            ]
            cur.executemany(
                "INSERT INTO coupons (code, discount_percent, `limit`, used_count, expiry_date) VALUES (%s,%s,%s,%s,%s)",
                coupons
            )
            print(f"✅ Seeded {len(coupons)} coupons")

            # ── Blog Posts ───────────────────────────────────────
            posts = [
                (
                    'Bí quyết chọn nguyên liệu tươi sạch cho bữa ăn gia đình',
                    'Việc chọn lựa nguyên liệu đầu vào quyết định 80% độ ngon của món ăn...',
                    json.dumps(['Việc chọn lựa nguyên liệu đầu vào quyết định 80% độ ngon của món ăn.', 'Hãy chọn những nguyên liệu tươi nhất từ các nhà cung cấp uy tín.'], ensure_ascii=False),
                    '2023-10-12', 'Mẹo nấu ăn',
                    'https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?q=80&w=1974&auto=format&fit=crop',
                    'Phạm Khánh Tài', 'https://picsum.photos/id/64/100/100', '5 phút đọc',
                    json.dumps(['#NguyênLiệu', '#CookTips'], ensure_ascii=False)
                ),
                (
                    '10 Cách Ăn Uống Lành Mạnh Mỗi Ngày Để Duy Trì Vóc Dáng',
                    'Xây dựng một chế độ ăn uống lành mạnh không có nghĩa là bạn phải từ bỏ hoàn toàn những món ăn yêu thích.',
                    json.dumps(['Xây dựng một chế độ ăn uống lành mạnh không có nghĩa là bạn phải từ bỏ hoàn toàn những món ăn yêu thích.'], ensure_ascii=False),
                    '2024-05-22', 'Sống khỏe',
                    'https://images.unsplash.com/photo-1512621776951-a57141f2eefd?q=80&w=2070&auto=format&fit=crop',
                    'Phạm Khánh Tài', 'https://picsum.photos/id/64/100/100', '8 phút đọc',
                    json.dumps(['#HealthyLife', '#Nutrition', '#FoodTips'], ensure_ascii=False)
                ),
            ]
            cur.executemany(
                """INSERT INTO blog_posts
                   (title, excerpt, content, post_date, category, image,
                    author_name, author_avatar, author_read_time, tags)
                   VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                posts
            )
            print(f"✅ Seeded {len(posts)} blog posts")

        print("\n🎉 Database seeding completed successfully!")
    except Exception as e:
        print(f"❌ Seed error: {e}")
        raise
    finally:
        conn.close()


if __name__ == '__main__':
    seed()
