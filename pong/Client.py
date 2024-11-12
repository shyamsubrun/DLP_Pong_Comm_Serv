import socket
import threading
import tkinter as tk
from ClientThread import PongGame

class PongClient:
    def __init__(self, username, server_ip, port):
        self.username = username
        self.server_ip = server_ip
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((server_ip, port))

        # Lancer le jeu
        self.game = PongGame(self)
        self.listen_thread = threading.Thread(target=self.receive_data)
        self.listen_thread.daemon = True
        self.listen_thread.start()

    def receive_data(self):
        while True:
            try:
                data = self.socket.recv(1024).decode('utf-8')
                if data:
                    self.game.update_from_server(data)
            except ConnectionResetError:
                print("Connexion au serveur perdue")
                break

    def send_data(self, message):
        try:
            self.socket.sendall(message.encode('utf-8'))
        except socket.error:
            print("Impossible d'envoyer le message au serveur")

    def close(self):
        self.socket.close()

if __name__ == "__main__":
    username = input("Entrez votre nom d'utilisateur : ")
    server_ip = input("Entrez l'IP du serveur : ")
    client = PongClient(username, server_ip, 59001)

    # Lancer l'interface graphique et le jeu
    client.game.run_game()
