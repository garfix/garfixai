import socket
import threading

class TextService:
    def __init__(self, host='localhost', port=8642):
        self.host = host
        self.port = port
        self.running = False
        self.commands = {
            "start": self.start_service,
            "stop": self.stop_service,
            "status": self.get_status,
            "help": self.show_help,
        }

    def start_service(self):
        if self.running:
            return "Service is already running."
        self.running = True
        return "Service started successfully."

    def stop_service(self):
        if not self.running:
            return "Service is not running."
        self.running = False
        return "Service stopped successfully."

    def get_status(self):
        return "Service is running." if self.running else "Service is stopped."

    def show_help(self):
        return "Available commands: start, stop, status, help"

    def handle_client(self, client_socket):
        with client_socket as sock:
            sock.sendall(b"Welcome to the text-based service. Type 'help' for commands.\n")
            while True:
                try:
                    data = sock.recv(1024).decode('utf-8').strip()
                    if not data:
                        break

                    if data in self.commands:
                        response = self.commands[data]()
                    else:
                        response = f"Unknown command: {data}. Type 'help' for available commands."

                    sock.sendall((response + "\n").encode('utf-8'))

                    if data == "stop":
                        break
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

if __name__ == "__main__":
    service = TextService()
    service.start()
