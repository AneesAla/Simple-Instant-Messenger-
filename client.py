import socket
import threading
import tkinter as tk
from tkinter import scrolledtext


class ChatClient:
    def __init__(self, root):
        self.root = root
        self.root.title("Instant Messaging - User2")

        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD)
        self.text_area.pack(padx=20, pady=5, expand=True, fill="both")
        self.text_area.config(state="disabled", font=("Arial", 12))

        self.msg_frame = tk.Frame(root)
        self.msg_frame.pack(padx=20, pady=5, fill=tk.X)

        self.msg_entry = tk.Entry(self.msg_frame, font=("Arial", 12))
        self.msg_entry.pack(side=tk.LEFT, expand=True, fill=tk.X)
        self.msg_entry.bind("<Return>", self.send_message)

        self.send_button = tk.Button(
            self.msg_frame, text="Send", command=self.send_message
        )
        self.send_button.pack(side=tk.RIGHT, padx=(5, 0))

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_ip = ""
        self.server_port = 9998
        self.client.connect((self.server_ip, self.server_port))

        self.receive_thread = threading.Thread(target=self.receive_messages)
        self.receive_thread.start()

    def send_message(self, event=None):
        message = self.msg_entry.get()
        self.msg_entry.delete(0, tk.END)
        if message == "quit":
            self.client.close()
            self.root.quit()
        else:
            self.client.send(message.encode("utf-8"))
            self.update_chat_window("You", message)

    def receive_messages(self):
        while True:
            try:
                msg = self.client.recv(1024).decode("utf-8")
                if msg == "quit":
                    self.client.close()
                    break
                self.update_chat_window("User1", msg)
            except Exception as e:
                print("An error occurred:", e)
                break

    def update_chat_window(self, sender, message):
        self.text_area.config(state="normal")
        self.text_area.insert("end", f"{sender}: {message}\n")
        self.text_area.yview("end")
        self.text_area.config(state="disabled")


root = tk.Tk()
app = ChatClient(root)
root.mainloop()
