import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, simpledialog, messagebox

class ChatClient:
    def __init__(self, host='localhost', port=8093):
        self.host = host
        self.port = port
        self.socket = None
        self.running = True
        
        # GUI setup
        self.root = tk.Tk()
        self.root.title("Chat Client")
        self.root.geometry("500x400")
        
        # Title
        title = tk.Label(self.root, text="Chat Client", font=("Arial", 14, "bold"))
        title.pack(pady=10)
        
        # Status
        self.status_label = tk.Label(self.root, text="Kết nối...", fg="blue")
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
        
        # Connect thread
        connect_thread = threading.Thread(target=self.connect_to_server, daemon=True)
        connect_thread.start()
        
        # Listen thread
        listen_thread = threading.Thread(target=self.listen_messages, daemon=True)
        listen_thread.start()
    
    def connect_to_server(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            self.log_message("System", "Kết nối thành công tới server!")
            self.status_label.config(text="Đã kết nối", fg="green")
        except Exception as e:
            self.log_message("Error", f"Lỗi kết nối: {str(e)}")
            self.status_label.config(text="Kết nối thất bại", fg="red")
    
    def listen_messages(self):
        while self.running and self.socket:
            try:
                self.socket.settimeout(1)
                message = self.socket.recv(1024).decode('utf-8')
                if message:
                    self.log_message("Server", message)
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
        
        if self.socket:
            try:
                self.socket.send(message.encode('utf-8'))
                self.log_message("Client", message)
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
        if self.socket:
            self.socket.close()
        self.root.quit()
    
    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self.close_connection)
        self.root.mainloop()

if __name__ == "__main__":
    client = ChatClient()
    client.run()
