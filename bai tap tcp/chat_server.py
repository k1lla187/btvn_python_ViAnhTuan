import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, simpledialog, messagebox
import time

class ChatServer:
    def __init__(self, host='localhost', port=8093):
        self.host = host
        self.port = port
        self.server = None
        self.connection = None
        self.running = True
        
        # GUI setup
        self.root = tk.Tk()
        self.root.title("Chat Server")
        self.root.geometry("500x400")
        
        # Title
        title = tk.Label(self.root, text="Chat Server", font=("Arial", 14, "bold"))
        title.pack(pady=10)
        
        # Status
        self.status_label = tk.Label(self.root, text="Chờ kết nối...", fg="blue")
        self.status_label.pack()
        
        # Chat area
        self.chat_area = scrolledtext.ScrolledText(self.root, height=15, width=60, state='disabled')
        self.chat_area.pack(padx=10, pady=10)
        
        # Input frame
        frame = tk.Frame(self.root)
        frame.pack(padx=10, pady=5)
        
        self.entry = tk.Entry(frame, width=45)
        self.entry.pack(side=tk.LEFT, padx=5)
        self.entry.bind('<Return>', lambda e: self.send_message())
        
        send_btn = tk.Button(frame, text="Gửi", command=self.send_message)
        send_btn.pack(side=tk.LEFT)
        
        close_btn = tk.Button(self.root, text="Đóng", command=self.close_connection)
        close_btn.pack(pady=10)
        
        # Start server thread
        server_thread = threading.Thread(target=self.start_server, daemon=True)
        server_thread.start()
        
        # Listen thread
        listen_thread = threading.Thread(target=self.listen_messages, daemon=True)
        listen_thread.start()
        
    def start_server(self):
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server.bind((self.host, self.port))
            self.server.listen(1)
            self.log_message("Server", f"Đang lắng nghe trên port {self.port}...")
            
            self.connection, addr = self.server.accept()
            self.log_message("System", f"Client kết nối từ {addr}")
            self.status_label.config(text=f"Đã kết nối: {addr}", fg="green")
            
        except Exception as e:
            self.log_message("Error", f"Lỗi: {str(e)}")
    
    def listen_messages(self):
        while self.running and self.connection:
            try:
                self.connection.settimeout(1)
                message = self.connection.recv(1024).decode('utf-8')
                if message:
                    self.log_message("Client", message)
                else:
                    break
            except socket.timeout:
                continue
            except:
                break
    
    def send_message(self):
        message = self.entry.get().strip()
        if not message:
            return
        
        if self.connection:
            try:
                self.connection.send(message.encode('utf-8'))
                self.log_message("Server", message)
                self.entry.delete(0, tk.END)
            except:
                messagebox.showerror("Lỗi", "Không thể gửi tin nhắn!")
    
    def log_message(self, sender, message):
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, f"{sender}: {message}\n")
        self.chat_area.see(tk.END)
        self.chat_area.config(state='disabled')
    
    def close_connection(self):
        self.running = False
        if self.connection:
            self.connection.close()
        if self.server:
            self.server.close()
        self.root.quit()
    
    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self.close_connection)
        self.root.mainloop()

if __name__ == "__main__":
    server = ChatServer()
    server.run()
