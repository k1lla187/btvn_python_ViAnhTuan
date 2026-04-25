import socket, re

def check(pw):
    if len(pw) < 6 or len(pw) > 12: return False
    if not re.search("[a-z]", pw): return False
    if not re.search("[0-9]", pw): return False
    if not re.search("[A-Z]", pw): return False
    if not re.search("[$#@]", pw): return False
    return True

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 8092))
server.listen(1)
conn, addr = server.accept()

data = conn.recv(1024).decode().split(',')
valid = [pw for pw in data if check(pw)]
conn.send(",".join(valid).encode())
conn.close()