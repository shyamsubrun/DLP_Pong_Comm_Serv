import socket
import threading
import time

class PongServer:
    def __init__(self, port=59001):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('', port))
        self.server_socket.listen(2)
        self.clients = []
        self.ball_position = [300, 200]
        self.ball_velocity = [5, 5]

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
                # Diffuser les mouvements de la balle et des raquettes aux autres clients
                self.broadcast(data, client_socket)
            except ConnectionResetError:
                break
        self.clients.remove(client_socket)
        client_socket.close()

    def broadcast(self, message, sender_socket):
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

            # Gérer les rebonds
            if self.ball_position[1] <= 0 or self.ball_position[1] >= 400:
                self.ball_velocity[1] = -self.ball_velocity[1]
            if self.ball_position[0] <= 0 or self.ball_position[0] >= 600:
                self.ball_velocity[0] = -self.ball_velocity[0]

            # Envoyer la position de la balle à tous les clients
            ball_data = f"BALL {self.ball_position[0]} {self.ball_position[1]}"
            self.broadcast(ball_data, None)

            time.sleep(0.03)  # Mettre à jour la balle toutes les 30 ms

if __name__ == "__main__":
    server = PongServer()
    server.accept_clients()
