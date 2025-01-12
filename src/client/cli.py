import os
import socket
from sys import argv
from dotenv import load_dotenv

def respond(argv: list[str], port: int):

    host = 'localhost'
    request = " ".join(argv[1:])

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((host, port))

            # Send the command to the server
            client_socket.sendall(request.encode('utf-8'))

            # Receive the response from the server
            response = client_socket.recv(1024).decode('utf-8')
            print(f"C: {response}")

    except ConnectionRefusedError:
        print(f"Failed to connect to server at {host}:{port}. Is the server running?")
    except Exception as e:
        print(f"An error occurred: {e}")


def main():
    # Load environment variables from .env file
    load_dotenv()

    port = int(os.getenv('PORT'))

    respond(argv, port)


if __name__ == "__main__":
    main()

