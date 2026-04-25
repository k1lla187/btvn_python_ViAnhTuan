import socket
import re
import threading
import time

def bai1_server():
    """Bài 1: Gửi nhận thông điệp cơ bản"""
    print("\n=== Bài 1: Socket TCP Cơ bản (Port 8090) ===")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('localhost', 8090))
    server.listen(1)
    print("Server đang đợi kết nối trên port 8090...")
    
    conn, addr = server.accept()
    print(f"Client kết nối từ {addr}")
    
    data = conn.recv(1024).decode()
    print(f"Server nhận được: {data}")
    
    conn.send("From SERVER TCP".encode())
    print("Server gửi: From SERVER TCP")
    
    conn.close()
    server.close()
    print("Kết nối đóng. Bài 1 hoàn tất!")

def bai2_server():
    """Bài 2: Tính tổng hai số"""
    print("\n=== Bài 2: Tính Tổng (Port 8091) ===")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('localhost', 8091))
    server.listen(1)
    print("Server đang đợi kết nối trên port 8091...")
    
    conn, addr = server.accept()
    print(f"Client kết nối từ {addr}")
    
    data = conn.recv(1024).decode().split(',')
    a = int(data[0].strip())
    b = int(data[1].strip())
    
    print(f"Server nhận được: a={a}, b={b}")
    
    tong = a + b
    conn.send(str(tong).encode())
    print(f"Server gửi: Tổng = {tong}")
    
    conn.close()
    server.close()
    print("Kết nối đóng. Bài 2 hoàn tất!")

def bai3_server():
    """Bài 3: Kiểm tra mật khẩu"""
    print("\n=== Bài 3: Kiểm Tra Mật Khẩu (Port 8092) ===")
    
    def check_password(pw):
        """Kiểm tra mật khẩu theo các tiêu chí"""
        if len(pw) < 6 or len(pw) > 12:
            return False
        if not re.search("[a-z]", pw):  # Ít nhất 1 chữ cái thường
            return False
        if not re.search("[0-9]", pw):  # Ít nhất 1 số
            return False
        if not re.search("[A-Z]", pw):  # Ít nhất 1 chữ cái hoa
            return False
        if not re.search("[$#@]", pw):  # Ít nhất 1 ký tự đặc biệt
            return False
        return True
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('localhost', 8092))
    server.listen(1)
    print("Server đang đợi kết nối trên port 8092...")
    
    conn, addr = server.accept()
    print(f"Client kết nối từ {addr}")
    
    passwords_input = conn.recv(1024).decode()
    print(f"Server nhận được: {passwords_input}")
    
    passwords = [pw.strip() for pw in passwords_input.split(',')]
    valid_passwords = [pw for pw in passwords if check_password(pw)]
    
    result = ",".join(valid_passwords)
    conn.send(result.encode())
    print(f"Server gửi mật khẩu hợp lệ: {result}")
    
    conn.close()
    server.close()
    print("Kết nối đóng. Bài 3 hoàn tất!")

def main():
    print("=" * 50)
    print("CHƯƠNG TRÌNH GỘP 4 BÀI TẬP SOCKET TCP")
    print("=" * 50)
    print("\nVui lòng chọn bài tập:")
    print("1. Bài 1: Socket TCP Cơ bản")
    print("2. Bài 2: Tính Tổng")
    print("3. Bài 3: Kiểm Tra Mật Khẩu")
    print("4. Bài 4: Chat GUI (Chạy chat_server.py)")
    print("0. Thoát")
    
    choice = input("\nNhập lựa chọn (0-4): ").strip()
    
    if choice == "1":
        bai1_server()
    elif choice == "2":
        bai2_server()
    elif choice == "3":
        bai3_server()
    elif choice == "4":
        print("\nBài 4: Chat GUI")
        print("Vui lòng chạy: python chat_server.py")
        print("Trên máy khác, chạy: python chat_client.py")
    elif choice == "0":
        print("Thoát chương trình!")
    else:
        print("Lựa chọn không hợp lệ!")

if __name__ == "__main__":
    main()
