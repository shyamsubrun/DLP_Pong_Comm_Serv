import socket
import sys
import time
from client_thread import ClientListener

class Server:
    def __init__(self, port):
        self.listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listener.bind(('', port))
        self.listener.listen(5)
        print(f"Listening on port {port}")
        self.clients_sockets = []

    def run(self):
        while True:
            print("Waiting for new clients...")
            try:
                client_socket, client_address = self.listener.accept()
            except socket.error:
                sys.exit("Cannot connect clients")
            self.clients_sockets.append(client_socket)
            print("Starting thread for client:", client_address)
            client_thread = ClientListener(self, client_socket, client_address)
            client_thread.start()
            time.sleep(0.1)

    def remove_socket(self, socket):
        if socket in self.clients_sockets:
            self.clients_sockets.remove(socket)

    def echo(self, data):
        print("Broadcasting:", data)
        for sock in self.clients_sockets:
            try:
                sock.sendall(data.encode("UTF-8"))
            except socket.error:
                print("Failed to send message")

if __name__ == "__main__":
    server = Server(59001)
    server.run()
