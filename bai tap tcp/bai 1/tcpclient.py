import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 8090))
client.send("From CLIENT TCP".encode())
print(f"Server phản hồi: {client.recv(1024).decode()}")
client.close()