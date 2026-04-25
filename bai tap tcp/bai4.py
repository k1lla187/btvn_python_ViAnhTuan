# Cấu trúc gợi ý cho GUI Chat (Server hoặc Client)
import tkinter as tk
from tkinter import scrolledtext

def send_message():
    msg = entry.get()
    # Code gửi tin nhắn qua socket tại đây
    chat_area.insert(tk.END, "Me: " + msg + "\n")
    entry.delete(0, tk.END)

root = tk.Tk()
chat_area = scrolledtext.ScrolledText(root)
chat_area.pack()
entry = tk.Entry(root, width=50)
entry.pack()
btn = tk.Button(root, text="Send", command=send_message)
btn.pack()
root.mainloop()