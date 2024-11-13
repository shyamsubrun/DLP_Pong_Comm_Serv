import socket
import threading
import time
import random

# Dimensions du jeu
LARGEUR = 600
HAUTEUR = 400
VITESSE_BALLE_X = 1
VITESSE_BALLE_Y = 2
RAQUETTE_HAUTEUR = 80

class PongServer:
    def __init__(self, port=59001):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('', port))
        self.server_socket.listen(2)
        self.clients = []
        self.ball_position = [300, 200]
        self.ball_velocity = [VITESSE_BALLE_X * random.choice([-1, 1]), VITESSE_BALLE_Y * random.choice([-1, 1])]
        self.paddle_positions = [200, 200]

    def accept_clients(self):
        while len(self.clients) < 2:
            client_socket, addr = self.server_socket.accept()
            self.clients.append(client_socket)
            print(f"Connexion établie avec {addr}")
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()
        self.update_ball()

    def handle_client(self, client_socket):
        while True:
            try:
                data = client_socket.recv(1024).decode('utf-8')
                if not data:
                    break
                print("Commande reçue sur le serveur :", data)
                if data == "MOVE LEFT UP":
                    self.update_paddle(0, self.paddle_positions[0] - 20)
                elif data == "MOVE LEFT DOWN":
                    self.update_paddle(0, self.paddle_positions[0] + 20)
                elif data == "MOVE RIGHT UP":
                    self.update_paddle(1, self.paddle_positions[1] - 20)
                elif data == "MOVE RIGHT DOWN":
                    self.update_paddle(1, self.paddle_positions[1] + 20)
                self.broadcast(data, client_socket)
            except ConnectionResetError:
                break
        self.clients.remove(client_socket)
        client_socket.close()

    def broadcast(self, message, sender_socket=None):
        for client in self.clients:
            if client != sender_socket:
                try:
                    client.sendall(message.encode('utf-8'))
                except socket.error:
                    client.close()
                    self.clients.remove(client)

    def update_ball(self):
        while True:
            self.ball_position[0] += self.ball_velocity[0]
            self.ball_position[1] += self.ball_velocity[1]
            if self.ball_position[1] <= 0 or self.ball_position[1] >= HAUTEUR:
                self.ball_velocity[1] = -self.ball_velocity[1]
            if 0 <= self.ball_position[0] <= 25:
                if (self.paddle_positions[0] - 20) <= self.ball_position[1] <= (self.paddle_positions[0] + RAQUETTE_HAUTEUR + 20):
                    self.ball_velocity[0] = -self.ball_velocity[0]
                    self.broadcast("TOUCHEZ GAUCHE")
                else:
                    self.ball_position = [LARGEUR // 2, HAUTEUR // 2]
                    self.ball_velocity = [VITESSE_BALLE_X * random.choice([-1, 1]), VITESSE_BALLE_Y * random.choice([-1, 1])]
            elif LARGEUR - 25 <= self.ball_position[0] <= LARGEUR:
                if (self.paddle_positions[1] - 20) <= self.ball_position[1] <= (self.paddle_positions[1] + RAQUETTE_HAUTEUR + 20):
                    self.ball_velocity[0] = -self.ball_velocity[0]
                    self.broadcast("TOUCHEZ DROIT")
                else:
                    self.ball_position = [LARGEUR // 2, HAUTEUR // 2]
                    self.ball_velocity = [VITESSE_BALLE_X * random.choice([-1, 1]), VITESSE_BALLE_Y * random.choice([-1, 1])]
            ball_data = f"BALL {int(self.ball_position[0])} {int(self.ball_position[1])}"
            self.broadcast(ball_data)
            time.sleep(0.03)

    def update_paddle(self, player, position):
        if player == 0:
            self.paddle_positions[0] = position
            self.broadcast(f"UPDATE LEFT PADDLE {self.paddle_positions[0]}")
        elif player == 1:
            self.paddle_positions[1] = position
            self.broadcast(f"UPDATE RIGHT PADDLE {self.paddle_positions[1]}")

if __name__ == "__main__":
    server = PongServer()
    server.accept_clients()
