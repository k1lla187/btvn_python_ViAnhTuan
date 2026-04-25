import socket
import time

def bai1_client():
    """Bài 1: Gửi nhận thông điệp cơ bản"""
    print("\n=== Bài 1: Socket TCP Cơ bản (Port 8090) ===")
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client.connect(('localhost', 8090))
        print("Client kết nối thành công tới server")
        
        client.send("From CLIENT TCP".encode())
        print("Client gửi: From CLIENT TCP")
        
        response = client.recv(1024).decode()
        print(f"Client nhận được: {response}")
        
    except ConnectionRefusedError:
        print("Lỗi: Không thể kết nối tới server. Chắc chắn server đang chạy?")
    finally:
        client.close()
    
    print("Bài 1 hoàn tất!")

def bai2_client():
    """Bài 2: Tính tổng hai số"""
    print("\n=== Bài 2: Tính Tổng (Port 8091) ===")
    
    try:
        a = int(input("Nhập số a: "))
        b = int(input("Nhập số b: "))
        
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('localhost', 8091))
        print("Client kết nối thành công tới server")
        
        message = f"{a},{b}"
        client.send(message.encode())
        print(f"Client gửi: {message}")
        
        response = client.recv(1024).decode()
        print(f"Server trả về tổng: {response}")
        
    except ConnectionRefusedError:
        print("Lỗi: Không thể kết nối tới server. Chắc chắn server đang chạy?")
    except ValueError:
        print("Lỗi: Vui lòng nhập số nguyên hợp lệ!")
    finally:
        client.close()
    
    print("Bài 2 hoàn tất!")

def bai3_client():
    """Bài 3: Kiểm tra mật khẩu"""
    print("\n=== Bài 3: Kiểm Tra Mật Khẩu (Port 8092) ===")
    print("\nYêu cầu mật khẩu:")
    print("- Ít nhất 1 chữ cái thường [a-z]")
    print("- Ít nhất 1 chữ cái hoa [A-Z]")
    print("- Ít nhất 1 số [0-9]")
    print("- Ít nhất 1 ký tự đặc biệt [$ # @]")
    print("- Độ dài: 6-12 ký tự")
    print("\nVí dụ: Abc123@1,aF1#2w3E*,2We3345")
    
    try:
        passwords_input = input("\nNhập mật khẩu (phân tách bởi dấu phẩy): ")
        
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('localhost', 8092))
        print("Client kết nối thành công tới server")
        
        client.send(passwords_input.encode())
        print(f"Client gửi: {passwords_input}")
        
        response = client.recv(1024).decode()
        if response:
            print(f"Mật khẩu hợp lệ: {response}")
        else:
            print("Không có mật khẩu nào hợp lệ!")
        
    except ConnectionRefusedError:
        print("Lỗi: Không thể kết nối tới server. Chắc chắn server đang chạy?")
    finally:
        client.close()
    
    print("Bài 3 hoàn tất!")

def main():
    print("=" * 50)
    print("CHƯƠNG TRÌNH GỘP 4 BÀI TẬP SOCKET TCP")
    print("=" * 50)
    print("\nVui lòng chọn bài tập:")
    print("1. Bài 1: Socket TCP Cơ bản")
    print("2. Bài 2: Tính Tổng")
    print("3. Bài 3: Kiểm Tra Mật Khẩu")
    print("4. Bài 4: Chat GUI (Chạy chat_client.py)")
    print("0. Thoát")
    
    choice = input("\nNhập lựa chọn (0-4): ").strip()
    
    if choice == "1":
        bai1_client()
    elif choice == "2":
        bai2_client()
    elif choice == "3":
        bai3_client()
    elif choice == "4":
        print("\nBài 4: Chat GUI")
        print("Vui lòng chạy: python chat_client.py")
    elif choice == "0":
        print("Thoát chương trình!")
    else:
        print("Lựa chọn không hợp lệ!")

if __name__ == "__main__":
    main()
