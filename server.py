import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("192.168.50.198", 9998))
server.listen()

print("Waiting for user2 to connect...")

client, addr = server.accept()
print(f"User2 connected from {addr}")

done = False

while not done:
    # Receive messages from user2
    user2_message = client.recv(1024).decode('utf-8')

    if user2_message == 'quit':
        print("User2 has exited. Closing connection.")
        break

    print(f"User2: {user2_message}")

    # Reply to user2
    user1_reply = input("User1 Reply: ")
    client.send(user1_reply.encode('utf-8'))

    if user1_reply == 'quit':
        print("User1 has exited. Closing connection.")
        break

client.close()
server.close()

