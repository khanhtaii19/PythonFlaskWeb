# Đánh giá thiếu sót / sai sót dự án Flask Fullstack

Ngày đánh giá: 2026-03-18

## 1) Bảo mật & phân quyền (mức nghiêm trọng cao)

1. **Nhiều API nhạy cảm chưa có middleware auth/admin**
   - `GET /api/auth/users` trả toàn bộ danh sách user nhưng route không gắn `auth_required` hoặc `admin_required`.
   - CRUD sản phẩm, tạo blog, xem/tạo/cập nhật đơn đều không bắt buộc token ở lớp route.
   - Rủi ro: lộ dữ liệu người dùng, sửa/xóa dữ liệu trái phép.

2. **CORS đang mở toàn bộ origin**
   - `CORS(app)` trong `server.py` chưa giới hạn theo biến môi trường `CORS_ORIGIN`.
   - Rủi ro: tăng bề mặt tấn công cross-origin.

3. **JWT secret mặc định yếu**
   - `JWT_SECRET` fallback là `'secret_key'`.
   - Rủi ro: dễ bị giả mạo token nếu deploy mà quên cấu hình `.env`.

4. **Thông báo lỗi trả thẳng exception ra client**
   - Nhiều controller trả `{'message': str(e)}`.
   - Rủi ro: lộ chi tiết DB/schema/stack nội bộ.

## 2) Tính đúng đắn dữ liệu & race condition

5. **Lấy bản ghi vừa insert bằng cách "ORDER BY created_at DESC LIMIT 1"**
   - Xảy ra ở tạo product/blog/order.
   - Trong môi trường nhiều request đồng thời có thể lấy nhầm bản ghi của request khác.

6. **Schema dùng UUID nhưng code vẫn thử `LAST_INSERT_ID()`**
   - Trong `create_product`, có câu query `SELECT * FROM products WHERE id = LAST_INSERT_ID()` rồi mới query khác.
   - Đây là chỉ dấu logic không nhất quán (UUID != auto increment).

7. **Order không có khóa ngoại user_id**
   - Bảng `orders` không khai báo FK tới `users`.
   - Có thể tạo đơn với `user_id='guest'` hoặc user không tồn tại, gây dữ liệu mồ côi.

8. **Thiếu transaction cho create_order**
   - Tạo order + order_items không dùng transaction tường minh.
   - Dù `autocommit=True` đang bật, nếu lỗi giữa chừng có thể còn dữ liệu bán phần.

## 3) API contract, validation và vận hành

9. **Document API lệch implementation**
   - Tài liệu ghi update status đơn là `PATCH /api/orders/:id/status` + JWT Admin.
   - Code đang dùng `PUT` và không gắn middleware auth/admin.

10. **Thiếu validation nghiệp vụ**
    - Chưa kiểm tra giá âm, stock âm, định dạng email/sđt, `status` hợp lệ, coupon hết hạn, tồn kho trước khi đặt hàng...

11. **Mật khẩu admin có cơ chế bypass hash**
    - Nếu email trùng `ADMIN_EMAIL` thì có thể đăng nhập bằng `ADMIN_PASSWORD` env (plain text), không cần hash DB.
    - Nên cân nhắc khi deploy production.

12. **Thông điệp lỗi/response chưa nhất quán ngôn ngữ**
    - Ví dụ login sai mật khẩu trả `'Sai mat khau'` trong khi các message khác tiếng Anh.

## 4) Sai sót tài liệu cấu hình

13. **Tên biến môi trường DB trong docs không khớp code**
    - Docs dùng `DB_HOST/DB_PORT/DB_USER/...`.
    - Code đọc `MYSQL_HOST/MYSQL_PORT/MYSQL_USER/...`.
    - Kết quả: người mới setup theo docs có thể không kết nối DB đúng.

## 5) Đề xuất ưu tiên xử lý

### Ưu tiên P0 (làm ngay)
- Gắn `@auth_required`/`@admin_required` cho các route nhạy cảm.
- Giới hạn CORS theo `CORS_ORIGIN`.
- Bỏ trả lỗi raw exception ra client.
- Loại bỏ fallback JWT secret yếu ở môi trường production.

### Ưu tiên P1
- Chuẩn hóa flow insert: dùng ID tạo từ app (UUID), trả lại theo ID đó, không query "newest".
- Dùng transaction cho tạo đơn hàng.
- Thêm FK/constraint cần thiết và validation dữ liệu đầu vào.

### Ưu tiên P2
- Đồng bộ tài liệu setup/API với code thực tế.
- Chuẩn hóa ngôn ngữ/thông điệp lỗi.

