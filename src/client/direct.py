import socket

def respond(argv, host='localhost', port=8642):
    print(argv)
    request = " ".join(argv[1:])

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((host, port))
            print(f"Connected to server at {host}:{port}")

            # Receive welcome message from server
            welcome_message = client_socket.recv(1024).decode('utf-8')
            print(welcome_message)

            # while True:
            #     # Get input from the user
            #     command = input("Enter command: ")

            #     if not command:
            #         print("Please enter a command.")
            #         continue

            # Send the command to the server
            client_socket.sendall(request.encode('utf-8'))

            # Receive the response from the server
            response = client_socket.recv(1024).decode('utf-8')
            print(f"Server response: {response}")

            #     if command.lower() == "stop":
            #         print("Exiting client.")
            #         break
    except ConnectionRefusedError:
        print(f"Failed to connect to server at {host}:{port}. Is the server running?")
    except Exception as e:
        print(f"An error occurred: {e}")

# if __name__ == "__main__":
#     start_client()
