import socket
import threading
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog

# Connecting To Server
HOST = "127.0.0.1"
PORT = 55557
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))


# GUI Class for the Chat
class GUI:
    def __init__(self):
        self.window = tkinter.Tk()
        self.window.withdraw()

        # Login Window
        self.login = tkinter.Toplevel()
        self.login.title("Login")
        self.login.resizable(width=False, height=False)
        self.login.configure(width=400, height=300)
        self.pls = tkinter.Label(
            self.login,
            text="Please login to continue",
            justify=tkinter.CENTER,
            font="Helvetica 14 bold",
        )
        self.pls.place(relheight=0.15, relx=0.2, rely=0.07)
        self.labelName = tkinter.Label(self.login, text="Name: ", font="Helvetica 12")
        self.labelName.place(relheight=0.2, relx=0.1, rely=0.2)
        self.entryName = tkinter.Entry(self.login, font="Helvetica 14")
        self.entryName.place(relwidth=0.4, relheight=0.12, relx=0.35, rely=0.2)
        self.entryName.focus()
        self.go = tkinter.Button(
            self.login,
            text="CONTINUE",
            font="Helvetica 14 bold",
            command=lambda: self.goAhead(self.entryName.get()),
        )
        self.go.place(relx=0.4, rely=0.55)
        self.window.mainloop()

    def goAhead(self, name):
        self.login.destroy()
        self.layout(name)
        # The thread for receiving messages
        rcv = threading.Thread(target=self.receive)
        rcv.start()

    # The main layout of the chat
    def layout(self, name):
        self.name = name
        self.window.deiconify()
        self.window.title("CHATROOM")
        self.window.resizable(width=False, height=False)
        self.window.configure(width=470, height=550, bg="#17202A")
        self.labelHead = tkinter.Label(
            self.window,
            bg="#17202A",
            fg="#EAECEE",
            text=self.name,
            font="Helvetica 13 bold",
            pady=5,
        )
        self.labelHead.place(relwidth=1)
        self.line = tkinter.Label(self.window, width=450, bg="#ABB2B9")
        self.line.place(relwidth=1, rely=0.07, relheight=0.012)
        self.textCons = tkinter.scrolledtext.ScrolledText(
            self.window,
            width=20,
            height=2,
            bg="#17202A",
            fg="#EAECEE",
            font="Helvetica 14",
            padx=5,
            pady=5,
        )
        self.textCons.place(relheight=0.745, relwidth=1, rely=0.08)
        self.labelBottom = tkinter.Label(self.window, bg="#ABB2B9", height=80)
        self.labelBottom.place(relwidth=1, rely=0.825)
        self.entryMsg = tkinter.Entry(
            self.labelBottom, bg="#2C3E50", fg="#EAECEE", font="Helvetica 13"
        )
        self.entryMsg.place(relwidth=0.74, relheight=0.06, rely=0.008, relx=0.011)
        self.entryMsg.focus()
        self.buttonMsg = tkinter.Button(
            self.labelBottom,
            text="Send",
            font="Helvetica 10 bold",
            width=20,
            bg="#ABB2B9",
            command=lambda: self.sendButton(self.entryMsg.get()),
        )
        self.buttonMsg.place(relx=0.77, rely=0.008, relheight=0.06, relwidth=0.22)
        self.textCons.config(cursor="arrow")
        scrollbar = tkinter.Scrollbar(self.textCons)
        scrollbar.place(relheight=1, relx=0.974)
        scrollbar.config(command=self.textCons.yview)
        self.textCons.config(state=tkinter.DISABLED)

    # Function to receive messages
    def receive(self):
        while True:
            try:
                message = client.recv(1024).decode("ascii")
                if message == "NICK":
                    client.send(self.name.encode("ascii"))
                else:
                    self.textCons.config(state=tkinter.NORMAL)
                    self.textCons.insert(tkinter.END, message + "\n\n")
                    self.textCons.config(state=tkinter.DISABLED)
                    self.textCons.see(tkinter.END)
            except:
                print("An error occured!")
                client.close()
                break

    # Function to send messages
    def sendButton(self, msg):
        self.textCons.config(state=tkinter.DISABLED)
        self.msg = msg
        self.entryMsg.delete(0, tkinter.END)
        snd = threading.Thread(target=self.write)
        snd.start()

    # Function to send messages
    def write(self):
        message = f"{self.name}: {self.msg}"
        client.send(message.encode("ascii"))


g = GUI()
