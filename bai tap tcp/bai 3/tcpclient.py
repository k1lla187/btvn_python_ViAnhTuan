import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 8092))
client.send("Abc123@1,aF1#2w3E*,2We3345".encode())
print(f"Mật khẩu hợp lệ: {client.recv(1024).decode()}")