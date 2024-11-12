import socket
import threading
import time
import random  # Assure-toi que random est importé

# Dimensions du jeu
LARGEUR = 600
HAUTEUR = 400
VITESSE_BALLE_X = 5
VITESSE_BALLE_Y = 5
RAQUETTE_HAUTEUR = 80

class PongServer:
    def __init__(self, port=59001):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('', port))
        self.server_socket.listen(2)
        self.clients = []
        self.ball_position = [300, 200]
        self.ball_velocity = [VITESSE_BALLE_X * random.choice([-1, 1]), VITESSE_BALLE_Y * random.choice([-1, 1])]
        self.paddle_positions = [200, 200]  # Position des raquettes des 2 joueurs

    def accept_clients(self):
        while len(self.clients) < 2:
            client_socket, addr = self.server_socket.accept()
            self.clients.append(client_socket)
            print(f"Connexion établie avec {addr}")
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

        # Démarrer la mise à jour de la balle après que les deux joueurs sont connectés
        self.update_ball()

    def handle_client(self, client_socket):
        while True:
            try:
                data = client_socket.recv(1024).decode('utf-8')
                if not data:
                    break
                # Diffuser les mouvements des raquettes aux autres clients
                self.broadcast(data, client_socket)
            except ConnectionResetError:
                break
        self.clients.remove(client_socket)
        client_socket.close()

    def broadcast(self, message, sender_socket=None):
        """ Diffuse un message à tous les clients sauf l'expéditeur """
        for client in self.clients:
            if client != sender_socket:
                try:
                    client.sendall(message.encode('utf-8'))
                except socket.error:
                    client.close()
                    self.clients.remove(client)

    def update_ball(self):
        while True:
            # Mettre à jour la position de la balle
            self.ball_position[0] += self.ball_velocity[0]
            self.ball_position[1] += self.ball_velocity[1]

            # Vérifier la collision avec les murs
            if self.ball_position[1] <= 0 or self.ball_position[1] >= HAUTEUR:
                self.ball_velocity[1] = -self.ball_velocity[1]

            # Vérifier la collision avec les raquettes
            if self.ball_position[0] <= 20:  # Raquette gauche
                if self.paddle_positions[0] <= self.ball_position[1] <= self.paddle_positions[0] + RAQUETTE_HAUTEUR:
                    self.ball_velocity[0] = -self.ball_velocity[0]
            elif self.ball_position[0] >= LARGEUR - 20:  # Raquette droite
                if self.paddle_positions[1] <= self.ball_position[1] <= self.paddle_positions[1] + RAQUETTE_HAUTEUR:
                    self.ball_velocity[0] = -self.ball_velocity[0]

            # Vérifier si la balle sort du terrain
            if self.ball_position[0] <= 0 or self.ball_position[0] >= LARGEUR:
                # Reinitialiser la position de la balle (début du jeu)
                self.ball_position = [LARGEUR // 2, HAUTEUR // 2]
                self.ball_velocity = [VITESSE_BALLE_X * random.choice([-1, 1]), VITESSE_BALLE_Y * random.choice([-1, 1])]

            # Envoyer la position de la balle et des raquettes aux clients
            ball_data = f"BALL {self.ball_position[0]} {self.ball_position[1]}"
            paddle_data = f"PADDLE {self.paddle_positions[0]} {self.paddle_positions[1]}"
            self.broadcast(ball_data)
            self.broadcast(paddle_data)

            time.sleep(0.03)  # Mettre à jour la balle toutes les 30 ms

    def update_paddle(self, player, position):
        """ Met à jour la position de la raquette du joueur """
        if player == 0:
            self.paddle_positions[0] = position
        elif player == 1:
            self.paddle_positions[1] = position

if __name__ == "__main__":
    server = PongServer()
    server.accept_clients()
