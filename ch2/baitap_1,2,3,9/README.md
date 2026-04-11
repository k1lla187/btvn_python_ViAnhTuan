# HỆ THỐNG QUẢN LÝ NHÂN VIÊN CÔNG TY ABC

## 📋 GIỚI THIỆU CHƯƠNG TRÌNH

Hệ thống Quản lý Nhân viên (EMS) là một ứng dụng Python chuyên nghiệp được thiết kế để giải quyết trọn vẹn các yêu cầu về Lập trình hướng đối tượng (OOP). Chương trình tích hợp giao diện **WinForm** hiện đại, cơ chế lưu trữ dữ liệu bền vững và các nghiệp vụ nhân sự nâng cao như quản lý dự án, thăng chức và đền bù hợp đồng.

---

## 🎯 PHÂN TÍCH CHỨC NĂNG

Hệ thống được thiết kế để bao quát 4 nhóm chức năng cốt lõi của một phần mềm quản lý doanh nghiệp:

### 1. Quản trị Nhân sự Master-Detail
- **Quản lý đa dạng cấp bậc**: Hỗ trợ 3 loại hình nhân viên (Manager, Developer, Intern) với các thuộc tính đặc thù (ngôn ngữ lập trình, chuyên ngành, quy mô team).
- **Thăng chức thông minh**: Chuyển đổi linh hoạt giữa các cấp bậc (Intern -> Dev -> Manager) mà không làm mất dữ liệu lịch sử hiệu suất.
- **Thôi việc & Đền bù**: Tự động tính toán khoản đền bù hợp đồng (2 tháng lương tổng) khi cho nhân viên nghỉ việc.

### 2. Quản lý Tiền lương & Đãi ngộ
- **Công thức lương động**: Mỗi chức vụ có một thuật toán tính lương riêng, tự động áp dụng khi thăng chức.
- **Điều chỉnh lương**: Hỗ trợ cả tăng lương và giảm lương cơ bản (có cơ chế bảo vệ lương tối thiểu > 1 triệu VNĐ).
- **Báo cáo tài chính**: Thống kê tổng quỹ lương toàn công ty và danh sách Top 3 lương cao nhất.

### 3. Quản lý & Thống kê Dự án
- **Phân bổ dự án**: Mỗi nhân viên có thể tham gia tối đa 5 dự án.
- **Thống kê tải trọng**: Sắp xếp nhân viên dựa trên số lượng dự án họ đang tham gia (từ nhiều nhất đến ít nhất).
- **Tra cứu người tham gia**: Tìm kiếm nhanh tất cả nhân viên đang thực hiện một dự án cụ thể.

### 4. Lưu trữ & Tìm kiếm
- **Persistence (Bền vững)**: Dữ liệu được lưu trữ dưới dạng file JSON (`employees.json`), đảm bảo không bị mất sau khi đóng ứng dụng.
- **Tìm kiếm đa năng**: Hỗ trợ tìm nhân viên theo ID hoặc tên (tìm kiếm mờ - fuzzy search).

---

## 💻 PHÂN TÍCH MÃ NGUỒN (CODE ANALYSIS)

Dự án này là minh chứng điển hình cho việc áp dụng các chuẩn mực phần mềm chất lượng cao:

### 1. Áp dụng 4 Tính chất OOP
- **Tính Trừu tượng (Abstraction)**: Sử dụng lớp cha ảo `Employee` và `ABC` (Abstract Base Class) để định nghĩa bộ khung hành vi chung cho toàn bộ nhân sự.
- **Tính Kế thừa (Inheritance)**: Các lớp con (`Manager`, `Developer`, `Intern`) kế thừa các thuộc tính nền tảng từ `Employee`, giúp giảm thiểu mã nguồn trùng lặp.
- **Tính Đa hình (Polymorphism)**: Phương thức `calculate_salary()` được ghi đè (override) ở mỗi lớp con, cho phép hệ thống tính lương đúng cho từng người chỉ bằng một lệnh gọi duy nhất.
- **Tính Đóng gói (Encapsulation)**: Sử dụng `@property` và các tham số protected (`_field`) để bảo vệ dữ liệu, ngăn chặn việc gán giá trị sai (như tuổi < 18 hoặc điểm > 10).

### 2. Kiến trúc Module (Clean Code)
Dự án tuân thủ nguyên tắc **Separation of Concerns** (Phân tách trách nhiệm):
- **Models**: Định nghĩa dữ liệu và thực thể.
- **Services**: Giải quyết logic nghiệp vụ và tính toán.
- **UI**: Tách biệt hoàn toàn giao diện (CLI và GUI) khỏi logic xử lý.
- **Exceptions**: Hệ thống lỗi tùy chỉnh giúp kiểm soát các trường hợp ngoại lệ nghiệp vụ.

### 3. Modern Python Features
- **Type Hinting**: Sử dụng chú thích kiểu dữ liệu (Python 3.5+) giúp mã nguồn tự tường minh và giảm thiểu lỗi logic.
- **Unit Testing**: Hệ thống được kiểm thử tự động toàn diện qua module `unittest`, đảm bảo các chức năng HR và Tài chính hoạt động chính xác 100%.
- **Vietnamese Docstrings**: Toàn bộ mã nguồn được tài liệu hóa bằng tiếng Việt chuẩn, giải thích kỹ lưỡng các khái niệm kỹ thuật được áp dụng.

---

## 🔧 HƯỚNG DẪN CÀI ĐẶT & CHẠY

### 1. Cấu trúc Thư mục
```text
employee_management/
├── data/               # Cửa sổ lưu trữ file JSON
├── exceptions/         # Các định nghĩa lỗi tùy chỉnh
├── models/             # Định nghĩa lớp đối tượng nhân viên
├── services/           # Logic quản lý công ty và bảng lương
├── tests/              # Bộ kiểm thử tự động
├── ui/                 # Giao diện CLI và GUI con
├── utils/              # Tiện ích định dạng và kiểm tra
├── gui_main.py         # Điểm chạy giao diện WinForm (Chính)
└── main.py             # Điểm chạy giao diện dòng lệnh (CLI)
```

### 2. Cách chạy
- **Chạy Giao diện WinForm**: `python gui_main.py`
- **Chạy Giao diện dòng lệnh**: `python main.py`
- **Chạy Kiểm thử (Unit Test)**: `python -m unittest discover tests`

---

## 📝 GIẢI PHÁP CHO BÀI TẬP 1, 2, 3, 9
Dự án này là lời giải tổng hợp và nâng cao cho chuỗi bài tập:
- **Bài 1**: Xây dựng lớp đối tượng cơ bản.
- **Bài 2**: Quản lý danh sách đối tượng.
- **Bài 3**: Kế thừa và Đa hình trong quản lý lương.
- **Bài 9**: Xử lý ngoại lệ, File JSON và giao diện người dùng chuyên nghiệp.

---
**Người thực hiện**: Vi Anh Tuấn  
**Môn học**: Lập trình hướng đối tượng (OOP) – Python
