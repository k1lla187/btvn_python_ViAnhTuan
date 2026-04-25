import socket
import threading

# Cấu hình IP và Port (Có thể sửa thủ công)
# '0.0.0.0' cho phép lắng nghe từ tất cả các interface mạng trong LAN
HOST = '0.0.0.0' 
PORT = 12345

def handle_client(client_socket, address):
    print(f"[+] Kết nối mới từ {address}")
    try:
        while True:
            # Nhận dữ liệu từ client
            data = client_socket.recv(1024)
            if not data:
                break
            
            # Giải mã và in tin nhắn ra màn hình server
            message = data.decode('utf-8')
            print(f"[{address}] gửi: {message}")
            
    except ConnectionResetError:
        print(f"[-] Client {address} đã ngắt kết nối đột ngột.")
    finally:
        print(f"[-] Đóng kết nối với {address}")
        client_socket.close()

def start_server():
    # Tạo socket TCP
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Bind socket vào IP và Port
        server.bind((HOST, PORT))
        # Lắng nghe kết nối
        server.listen(5)
        
        # Lấy IP thật của máy trong mạng LAN để hiển thị cho người dùng biết
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        
        print(f"[*] Server đang chạy tại IP LAN: {local_ip}, Port: {PORT}")
        print(f"[*] Đang lắng nghe kết nối từ mọi client trong LAN...")

        while True:
            # Chấp nhận kết nối mới
            client_sock, addr = server.accept()
            # Tạo luồng mới để xử lý mỗi client riêng biệt (cho phép nhiều client cùng lúc)
            client_handler = threading.Thread(target=handle_client, args=(client_sock, addr))
            client_handler.start()
            
    except Exception as e:
        print(f"[!] Lỗi: {e}")
    finally:
        server.close()

if __name__ == "__main__":
    start_server()
