import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_ip = "192.168.50.198"
server_port = 9998

client.connect((server_ip, server_port))

done = False

while not done:
    # Send messages to user1
    user2_message = input("User2 Message: ")
    client.send(user2_message.encode('utf-8'))

    if user2_message == 'quit':
        print("User2 has exited. Closing connection.")
        break

    # Receive replies from user1
    user1_reply = client.recv(1024).decode('utf-8')

    if user1_reply == 'quit':
        print("User1 has exited. Closing connection.")
        break

    print(f"User1 Reply: {user1_reply}")

client.close()
