import socket
import threading


def client_thread(conn, addr):
    while True:
        try:
            message = conn.recv(1024).decode("utf-8")
            if message == "quit":
                print("Closing connection.")
                break
            if message:
                print(f"{addr}: {message}")
                conn.sendall(f"Server received: {message}".encode())
            else:
                break
        except:
            break

    conn.close()


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("", 9998))
server.listen()

done = False

while not done:
    client, addr = server.accept()
    print(f"Connected with {addr}")
    thread = threading.Thread(target=client_thread, args=(client, addr))
    thread.start()
