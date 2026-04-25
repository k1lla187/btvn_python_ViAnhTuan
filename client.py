import socket

# Cấu hình IP và Port của SERVER (Sửa thủ công tại đây)
# Nhập địa chỉ IP LAN của máy đóng vai trò Server
SERVER_IP = '127.0.0.1' 
PORT = 12345

def start_client():
    # Tạo socket TCP
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Kết nối tới server
        print(f"[*] Đang kết nối tới server {SERVER_IP}:{PORT}...")
        client.connect((SERVER_IP, PORT))
        print("[+] Kết nối thành công! Bạn có thể bắt đầu gửi tin nhắn.")
        print("[*] Nhập 'quit' hoặc 'exit' để thoát.")

        while True:
            # Nhập tin nhắn từ bàn phím
            message = input("Bạn: ")
            
            if message.lower() in ['quit', 'exit']:
                break
            
            if not message.strip():
                continue

            # Gửi gói tin văn bản (được mã hóa UTF-8)
            client.send(message.encode('utf-8'))
            
    except ConnectionRefusedError:
        print("[!] Không thể kết nối tới Server. Hãy chắc chắn Server đã chạy và IP/Port đúng.")
    except Exception as e:
        print(f"[!] Lỗi: {e}")
    finally:
        client.close()
        print("[*] Đã đóng kết nối.")

if __name__ == "__main__":
    start_client()
