import socket
import threading
import time
import random
from ClientThread import ClientListener

# Dimensions du jeu
LARGEUR = 600
HAUTEUR = 400
VITESSE_BALLE_X = 5
VITESSE_BALLE_Y = 5

class PongServer:
    def __init__(self, port):
        self.listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listener.bind(('', port))
        self.listener.listen(2)
        print(f"Listening on port {port}")
        self.clients = []
        self.balle_pos = [LARGEUR // 2, HAUTEUR // 2]
        self.vitesse_balle_x = VITESSE_BALLE_X * random.choice([-1, 1])
        self.vitesse_balle_y = VITESSE_BALLE_Y * random.choice([-1, 1])

    def run(self):
        print("Server running...")
        while len(self.clients) < 2:
            client_socket, client_address = self.listener.accept()
            print(f"Client connected: {client_address}")
            client_thread = ClientListener(self, client_socket)
            client_thread.start()
            self.clients.append(client_thread)

        while True:
            self.update_game()
            time.sleep(0.03)

    def update_game(self):
        # Déplacement de la balle
        self.balle_pos[0] += self.vitesse_balle_x
        self.balle_pos[1] += self.vitesse_balle_y

        # Collision avec le haut et le bas
        if self.balle_pos[1] <= 0 or self.balle_pos[1] >= HAUTEUR:
            self.vitesse_balle_y *= -1

        # Envoie de la position de la balle aux clients
        data = f"BALL {self.balle_pos[0]} {self.balle_pos[1]}"
        for client in self.clients:
            client.send(data)

if __name__ == "__main__":
    server = PongServer(59001)
    server.run()
