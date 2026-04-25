import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 8091))
server.listen(1)
conn, addr = server.accept()

data = conn.recv(1024).decode().split(',')
a, b = int(data[0]), int(data[1])
tong = a + b
conn.send(str(tong).encode())
conn.close()