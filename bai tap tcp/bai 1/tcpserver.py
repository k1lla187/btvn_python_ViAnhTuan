import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 8090))
server.listen(1)
print("Server đang đợi kết nối...")

conn, addr = server.accept()
data = conn.recv(1024).decode()
print(f"Nhận được: {data}")
conn.send("From SERVER TCP".encode())
conn.close()