import threading
import re
import time
import socket

class ClientListener(threading.Thread):
    def __init__(self, server, client_socket, address):
        super(ClientListener, self).__init__()
        self.server = server
        self.socket = client_socket
        self.address = address
        self.listening = True
        self.username = "No username"

    def run(self):
        while self.listening:
            try:
                data = self.socket.recv(1024).decode('UTF-8')
                if data:
                    self.handle_msg(data)
                else:
                    self.quit()
            except socket.error:
                print("Unable to receive data")
                self.quit()
            time.sleep(0.1)

    def quit(self):
        self.listening = False
        self.socket.close()
        self.server.remove_socket(self.socket)
        self.server.echo(f"{self.username} has quit.\n")

    def handle_msg(self, data):
        username_result = re.search('^USERNAME (.*)$', data)
        if username_result:
            self.username = username_result.group(1)
            self.server.echo(f"{self.username} has joined.\n")
        elif data == "QUIT":
            self.quit()
        else:
            self.server.echo(data)
