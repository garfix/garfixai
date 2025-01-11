import socket
import threading
from app.main import create_pipeline
from richard.entity.SentenceRequest import SentenceRequest

class TextService:
    def __init__(self, host='localhost', port=8642):
        self.host = host
        self.port = port


    def handle_client(self, client_socket):
        with client_socket as sock:
            while True:
                try:
                    data = sock.recv(1024).decode('utf-8').strip()
                    if not data:
                        break

                    self.pipeline = create_pipeline()

                    request = SentenceRequest(data)
                    response = self.pipeline.enter(request)

                    sock.sendall((response + "\n").encode('utf-8'))

                except Exception as e:
                    sock.sendall(f"Error: {str(e)}\n".encode('utf-8'))
                    break


    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind((self.host, self.port))
            server_socket.listen(5)
            print(f"Service listening on {self.host}:{self.port}")

            while True:
                try:
                    client_socket, addr = server_socket.accept()
                    print(f"Connection from {addr}")
                    client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
                    client_handler.start()
                except KeyboardInterrupt:
                    print("Shutting down the server.")
                    break


def main():
    TextService().start()


if __name__ == "__main__":
    main()

