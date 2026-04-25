# Chương Trình Gộp 4 Bài Tập Socket TCP

Chương trình này gộp 4 bài tập về Socket TCP/Client-Server:
- **Bài 1**: Socket TCP Cơ bản
- **Bài 2**: Tính Tổng Hai Số
- **Bài 3**: Kiểm Tra Mật Khẩu
- **Bài 4**: Chat GUI

## Cấu Trúc File

```
bai tap tcp/
├── main_server.py          # Server chính (Bài 1, 2, 3)
├── main_client.py          # Client chính (Bài 1, 2, 3)
├── chat_server.py          # Server Chat GUI (Bài 4)
├── chat_client.py          # Client Chat GUI (Bài 4)
└── README.md               # File này
```

## Hướng Dẫn Chạy

### Chạy Bài 1, 2, 3 (Socket TCP Cơ bản)

#### Trên Server (Terminal 1):
```bash
cd "d:\btvn_python_ViAnhTuan\bai tap tcp"
python main_server.py
```

Khi hỏi lựa chọn, nhập: `1`, `2`, hoặc `3`

#### Trên Client (Terminal 2):
```bash
cd "d:\btvn_python_ViAnhTuan\bai tap tcp"
python main_client.py
```

Khi hỏi lựa chọn, nhập: `1`, `2`, hoặc `3` (giống với server)

### Bài 1: Socket TCP Cơ bản

**Yêu cầu:**
- Client gửi "From CLIENT TCP"
- Server nhận và trả về "From SERVER TCP"

**Port:** 8090

**Kết quả:**
```
Server:
  Server nhận được: From CLIENT TCP
  Server gửi: From SERVER TCP

Client:
  Client gửi: From CLIENT TCP
  Client nhận được: From SERVER TCP
```

### Bài 2: Tính Tổng Hai Số

**Yêu cầu:**
- Client nhập 2 số nguyên a và b
- Server tính tổng a + b
- Server trả về tổng cho client

**Port:** 8091

**Ví dụ:**
```
Client nhập: a = 10, b = 20
Server trả về: 30
```

### Bài 3: Kiểm Tra Mật Khẩu

**Yêu cầu mật khẩu hợp lệ:**
- Ít nhất 1 chữ cái thường [a-z]
- Ít nhất 1 chữ cái hoa [A-Z]
- Ít nhất 1 số [0-9]
- Ít nhất 1 ký tự đặc biệt [$ # @]
- Độ dài: 6-12 ký tự

**Port:** 8092

**Cách nhập:**
- Client nhập các mật khẩu phân tách bởi dấu phẩy
- Server kiểm tra và trả về những mật khẩu hợp lệ

**Ví dụ:**
```
Input: Abc123@1,aF1#2w3E*,2We3345
Output: Abc123@1
```

**Giải thích:**
- `Abc123@1` ✓ (có chữ thường 'bc', hoa 'A', số '123', ký tự '@', độ dài 8)
- `aF1#2w3E*` ✗ (có ký tự '*' không nằm trong [$ # @])
- `2We3345` ✗ (không có ký tự đặc biệt [$ # @])

### Bài 4: Chat GUI

Bài 4 là chương trình chat giữa 2 máy tính với giao diện GUI

#### Chạy Server Chat (Terminal 1):
```bash
python chat_server.py
```

#### Chạy Client Chat (Terminal 2):
```bash
python chat_client.py
```

**Port:** 8093

**Tính năng:**
- Giao diện GUI sử dụng tkinter
- Hiển thị lịch sử trò chuyện
- Nhập tin nhắn và gửi bằng Enter hoặc nút "Gửi"
- Hiển thị trạng thái kết nối

---

## Lưu Ý Quan Trọng

1. **Chạy Server Trước**: Luôn chạy server trước khi chạy client
2. **Cùng Port**: Nếu port bị chiếm, chương trình sẽ báo lỗi
3. **Localhost**: Mặc định kết nối qua `localhost`. Để kết nối qua mạng, thay `'localhost'` bằng IP của server
4. **Cửa Sổ Chat**: Đóng cửa sổ chat để dừng chương trình

## Troubleshooting

### Lỗi: "Connection refused"
- Chắc chắn server đang chạy
- Kiểm tra cổng (port) có được sử dụng không

### Lỗi: "Address already in use"
- Một server khác đang sử dụng port
- Chờ một lúc hoặc thay đổi port trong code

### Chat không nhận được tin nhắn
- Kiểm tra kết nối internet (nếu kết nối qua mạng)
- Đảm bảo firewall không chặn port

## Các Tệp Cũ

Các file bài tập cũ vẫn còn trong thư mục:
- `bai 1/tcpserver.py`, `bai 1/tcpclient.py`
- `bai2/tcpserver.py`, `bai2/tcpclient.py`
- `bai 3/tcpserver.py`, `bai 3/tcpclient.py`
- `bai4.py`

Chúng có thể xóa nếu không cần thiết.

---

**Tác giả**: Student  
**Ngày tạo**: 2026  
**Phiên bản**: 1.0
