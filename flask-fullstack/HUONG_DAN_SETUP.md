# 🍽️ GourmetShop — Hướng dẫn Setup & Chạy dự án

> **Flask Fullstack** · Python + MySQL · Jinja2 Templates · Tailwind CSS

---

## 📋 Yêu cầu hệ thống

| Công cụ | Phiên bản tối thiểu | Kiểm tra |
|---|---|---|
| Python | 3.9+ | `python --version` |
| pip | 21+ | `pip --version` |
| MySQL | 8.0+ | `mysql --version` |
| Git (tuỳ chọn) | 2.x | `git --version` |

---

## 🗂️ Bước 1 — Giải nén dự án

```bash
# Giải nén file zip
unzip flask-fullstack.zip

# Vào thư mục dự án
cd flask-fullstack
```

Cấu trúc thư mục sau khi giải nén:

```
flask-fullstack/
├── server.py                  ← Khởi chạy ứng dụng
├── seed.py                    ← Tạo dữ liệu mẫu
├── requirements.txt           ← Các thư viện Python
├── .env                       ← Cấu hình môi trường
├── src/
│   ├── config/database.py     ← Kết nối & khởi tạo MySQL
│   ├── controllers/           ← Logic xử lý API
│   ├── middleware/auth.py     ← Xác thực JWT
│   └── routes/routes.py       ← Định nghĩa routes
└── templates/
    ├── base.html              ← Layout chung
    ├── components/            ← Header, Footer, Cart
    └── pages/                 ← Tất cả các trang
```

---

## 🐍 Bước 2 — Tạo môi trường ảo Python

> Môi trường ảo giúp tránh xung đột thư viện giữa các dự án.

```bash
# Tạo môi trường ảo
python -m venv venv

# Kích hoạt môi trường ảo
# ▶ Windows (CMD):
venv\Scripts\activate

# ▶ Windows (PowerShell):
venv\Scripts\Activate.ps1

# ▶ macOS / Linux:
source venv/bin/activate
```

Sau khi kích hoạt, terminal sẽ hiển thị `(venv)` ở đầu dòng:
```
(venv) C:\projects\flask-fullstack>
```

---

## 📦 Bước 3 — Cài đặt thư viện

```bash
pip install -r requirements.txt
```

Các thư viện sẽ được cài:
- `Flask` — Web framework chính
- `Flask-Cors` — Cho phép cross-origin requests
- `PyMySQL` — Kết nối MySQL từ Python
- `PyJWT` — Tạo và xác thực token đăng nhập
- `bcrypt` — Mã hoá mật khẩu
- `python-dotenv` — Đọc file `.env`

---

## 🗄️ Bước 4 — Chuẩn bị MySQL

### 4.1 — Đăng nhập MySQL

```bash
# Đăng nhập với tài khoản root
mysql -u root -p
# Nhập mật khẩu MySQL của bạn
```

### 4.2 — Tạo database

```sql
-- Tạo database với bộ ký tự UTF-8 (hỗ trợ tiếng Việt)
CREATE DATABASE gourmet_shop
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

-- Kiểm tra đã tạo thành công chưa
SHOW DATABASES;

-- Thoát MySQL
EXIT;
```

---

## ⚙️ Bước 5 — Cấu hình file `.env`

Mở file `.env` trong thư mục dự án và chỉnh sửa:

```env
# ── Database ──────────────────────────────
DB_HOST=localhost        # Địa chỉ MySQL (thường là localhost)
DB_PORT=3306             # Cổng MySQL (mặc định 3306)
DB_USER=root             # Tên đăng nhập MySQL của bạn
DB_PASSWORD=your_password_here   # ← Đổi thành mật khẩu thực của bạn
DB_NAME=gourmet_shop

# ── Bảo mật ───────────────────────────────
JWT_SECRET=your-super-secret-key-change-this   # ← Đổi thành chuỗi ngẫu nhiên

# ── Tài khoản Admin mặc định ──────────────
ADMIN_EMAIL=admin@shop.com
ADMIN_PASSWORD=admin123
```

> ⚠️ **Quan trọng:** Đổi `DB_PASSWORD` và `JWT_SECRET` trước khi chạy.

---

## 🌱 Bước 6 — Tạo bảng và seed dữ liệu mẫu

```bash
# Lệnh này sẽ:
# 1. Tạo tất cả các bảng MySQL (users, products, orders, ...)
# 2. Thêm dữ liệu mẫu (sản phẩm, danh mục, người dùng, blog)
python seed.py
```

Sau khi chạy xong, terminal sẽ hiển thị:
```
✅ Đã tạo 7 bảng thành công
✅ Đã seed 20 sản phẩm
✅ Đã seed 5 danh mục
✅ Đã seed 3 người dùng mẫu
✅ Đã seed 5 bài blog
```

### Tài khoản mẫu được tạo sẵn:

| Email | Mật khẩu | Vai trò |
|---|---|---|
| admin@shop.com | 123456 | Admin |
| vana@example.com | 123456 | Người dùng |
| thib@example.com | 123456 | Người dùng |

---

## 🚀 Bước 7 — Chạy ứng dụng

```bash
python server.py
```

Terminal sẽ hiển thị:
```
 * Running on http://0.0.0.0:5000
 * Debug mode: on
 * Restarting with stat
```

Mở trình duyệt và truy cập: **http://localhost:5000**

---

## 🌐 Các trang có sẵn

| URL | Mô tả |
|---|---|
| `http://localhost:5000/` | Trang chủ |
| `http://localhost:5000/products` | Danh sách sản phẩm |
| `http://localhost:5000/products/1` | Chi tiết sản phẩm |
| `http://localhost:5000/blog` | Danh sách blog |
| `http://localhost:5000/login` | Đăng nhập |
| `http://localhost:5000/register` | Đăng ký |
| `http://localhost:5000/checkout` | Thanh toán |
| `http://localhost:5000/orders` | Đơn hàng của tôi |
| `http://localhost:5000/profile` | Tài khoản |
| `http://localhost:5000/admin` | Quản trị (cần login admin) |
| `http://localhost:5000/health` | Kiểm tra server |

---

## 🔌 API Endpoints

| Method | URL | Mô tả | Auth |
|---|---|---|---|
| POST | `/api/auth/register` | Đăng ký | Không |
| POST | `/api/auth/login` | Đăng nhập | Không |
| GET | `/api/auth/me` | Thông tin cá nhân | JWT |
| GET | `/api/products` | Danh sách sản phẩm | Không |
| GET | `/api/products/:id` | Chi tiết sản phẩm | Không |
| GET | `/api/categories` | Danh mục | Không |
| GET | `/api/orders` | Đơn hàng của tôi | JWT |
| POST | `/api/orders` | Tạo đơn hàng | JWT |
| PATCH | `/api/orders/:id/status` | Cập nhật trạng thái | JWT Admin |
| GET | `/api/blog` | Danh sách bài viết | Không |
| GET | `/api/blog/:id` | Chi tiết bài viết | Không |
| GET | `/api/coupons` | Danh sách mã giảm giá | Không |

---

## 🛠️ Xử lý lỗi thường gặp

### ❌ Lỗi kết nối MySQL
```
pymysql.err.OperationalError: (2003, "Can't connect to MySQL server")
```
**Giải pháp:**
```bash
# Kiểm tra MySQL đang chạy chưa
# Windows:
net start MySQL80

# macOS (Homebrew):
brew services start mysql

# Linux:
sudo systemctl start mysql
```

---

### ❌ Lỗi sai mật khẩu MySQL
```
pymysql.err.OperationalError: (1045, "Access denied for user 'root'@'localhost'")
```
**Giải pháp:** Kiểm tra lại `DB_PASSWORD` trong file `.env`

---

### ❌ Lỗi module not found
```
ModuleNotFoundError: No module named 'flask'
```
**Giải pháp:**
```bash
# Đảm bảo môi trường ảo đang được kích hoạt (thấy "(venv)")
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows

# Cài lại thư viện
pip install -r requirements.txt
```

---

### ❌ Port 5000 đã được dùng
```
OSError: [Errno 98] Address already in use
```
**Giải pháp:**
```bash
# Chạy trên port khác (ví dụ 8000)
# Sửa dòng cuối trong server.py:
app.run(debug=True, host='0.0.0.0', port=8000)
```

---

### ❌ Lỗi JWT / Token
```
401 Unauthorized
```
**Giải pháp:** Đăng nhập lại tại `/login` để lấy token mới.

---

## 🔄 Lệnh hữu ích hàng ngày

```bash
# Kích hoạt môi trường ảo (cần làm mỗi lần mở terminal mới)
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows

# Chạy server
python server.py

# Reset toàn bộ dữ liệu mẫu
python seed.py

# Dừng server
Ctrl + C

# Thoát môi trường ảo
deactivate
```

---

## 📁 Tuỳ chỉnh giao diện

- **Màu sắc chính:** Tìm `#ff5c62` trong các file HTML để đổi màu coral
- **Logo/Tên cửa hàng:** Sửa trong `templates/components/header.html`
- **Footer:** Sửa trong `templates/components/footer.html`
- **Thêm trang mới:** Tạo file trong `templates/pages/`, thêm route vào `server.py`

---

*GourmetShop · Flask Fullstack · Python + MySQL + Jinja2*
