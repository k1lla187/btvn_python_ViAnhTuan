import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 8091))
client.send("10,20".encode()) # Ví dụ gửi 10 và 20
print(f"Tổng là: {client.recv(1024).decode()}")
client.close()