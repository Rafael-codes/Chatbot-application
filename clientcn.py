import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox


HOST = "127.0.0.1"
PORT = 5050

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client_socket.connect((HOST, PORT))
except ConnectionRefusedError:
    messagebox.showerror("Error", "Cannot connect to chatbot server. Run server.py first.")
    raise SystemExit


root = tk.Tk()
root.title("Chatbot")
root.geometry("500x500")
root.config(bg="white")

chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, bg="white", fg="black", font=("Arial", 11))
chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
chat_area.config(state=tk.DISABLED)

entry_frame = tk.Frame(root, bg="white")
entry_frame.pack(fill=tk.X, pady=5)

user_input = tk.Entry(entry_frame, font=("Arial", 12), width=40, relief="solid", bd=2)
user_input.pack(side=tk.LEFT, padx=5, pady=5, ipady=5, expand=True, fill=tk.X)

send_button = tk.Button(entry_frame, text="Send", font=("Arial", 11, "bold"), bg="#4CAF50", fg="white",
                        relief="raised", bd=3, width=10, command=lambda: send_message())
send_button.pack(side=tk.RIGHT, padx=5)


def send_message():
    msg = user_input.get().strip()
    if msg == "":
        return
    chat_area.config(state=tk.NORMAL)
    chat_area.insert(tk.END, f"You: {msg}\n", "user")
    chat_area.tag_config("user", foreground="green")
    chat_area.config(state=tk.DISABLED)
    user_input.delete(0, tk.END)
    client_socket.send(msg.encode())

def receive_messages():
    while True:
        try:
            response = client_socket.recv(1024).decode()
            if not response:
                break
            chat_area.config(state=tk.NORMAL)
            chat_area.insert(tk.END, f"Bot: {response}\n", "bot")
            chat_area.tag_config("bot", foreground="red")
            chat_area.config(state=tk.DISABLED)
            chat_area.see(tk.END)
        except:
            break

threading.Thread(target=receive_messages, daemon=True).start()

root.mainloop()
client_socket.close()
