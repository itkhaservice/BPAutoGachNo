# BP Auto Gach No (v1.0.0)

Công cụ tự động hóa quy trình gạch nợ (cập nhật trạng thái "Đã thanh toán") cho hệ thống Quản lý vận hành Kha Service.

## 🌟 Tính năng chính
- **Tự động hóa hoàn toàn:** Tự động đăng nhập, tìm kiếm căn hộ và cập nhật trạng thái báo phí.
- **Cơ chế Xác minh (Verify):** Đảm bảo trạng thái được cập nhật thành công trên giao diện trước khi lưu, tránh sai sót dữ liệu.
- **Chế độ Ẩn danh (Fresh Session):** Mỗi lượt chạy là một phiên làm việc sạch, không lưu cookies hay thông tin đăng nhập sau khi đóng.
- **Tốc độ & Ổn định:** Khởi động nhanh, tự động xử lý lỗi và tiếp tục danh sách nếu gặp sự cố ở một căn hộ.
- **Giao diện hiện đại:** Điều khiển qua giao diện web trực quan, tích hợp nhật ký hoạt động thời gian thực.

## 🛠 Hướng dẫn sử dụng

### 1. Chuẩn bị dữ liệu
- File dữ liệu mẫu: `data.xlsx`.
- **Sheet "Data":** Chứa danh sách cần gạch nợ.
    - Cột 1: Mã căn hộ (Ví dụ: 01.01).
    - Cột 2: Kỳ báo phí (Định dạng: MM/YYYY, ví dụ: 04/2026).

### 2. Cài đặt
- Tải file bộ cài đặt: [BPAutoGachNo_Setup.exe](https://github.com/itkhaservice/BPAutoGachNo/releases).
- Chạy file Setup để cài đặt ứng dụng vào máy tính.
- Biểu tượng **BP Auto Gach No** sẽ xuất hiện trên màn hình Desktop.

### 3. Thực hiện gạch nợ
1. Mở ứng dụng.
2. Nhập **Email** và **Mật khẩu** tài khoản quản trị hệ thống.
3. Nhập danh sách căn hộ và kỳ phí (hoặc copy từ Excel dán vào bảng trên giao diện).
4. Nhấn **BẮT ĐẦU CHẠY**.
5. Theo dõi tiến trình qua cửa sổ trình duyệt tự động và khung nhật ký (Log).
6. Sau khi hoàn tất, trình duyệt sẽ tự động đóng và xóa sạch phiên làm việc.

## 👨‍💻 Thông tin phát triển
- **Phiên bản:** 1.0.0
- **Nguồn:** CMTHANG
- **Công nghệ:** Python, Playwright, HTML/JS.

---
*Lưu ý: Vui lòng kiểm tra kỹ danh sách trước khi chạy để đảm bảo tính chính xác của dữ liệu tài chính.*
