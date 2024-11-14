import socket
import sys
import time
import threading
import random
from ClientThread import ClientListener

VITESSE_BALLE_X = 5
VITESSE_BALLE_Y = 5

class Server():
    def __init__(self, port):
        self.vitesse_balle_x = VITESSE_BALLE_X * random.choice([-1, 1])
        self.vitesse_balle_y = VITESSE_BALLE_Y * random.choice([-1, 1])
        self.pos_ball = "BALL " + str(self.vitesse_balle_x) + " " + str(self.vitesse_balle_y) + " "
        
        self.listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listener.bind(('', port))
        self.listener.listen(1)
        print("Listening on port", port)
        
        self.clients_sockets = []
        self.client_roles = {}  # Dictionnaire pour assigner les rôles aux clients
        self.ball_thread_started = False
        self.ball_thread_running = True

    def run(self):
        while True:
            try:
                (client_socket, client_address) = self.listener.accept()
            except socket.error:
                sys.exit("Cannot connect clients")
                
            # Attribution du rôle (raquette gauche ou droite)
            if len(self.clients_sockets) == 0:
                self.client_roles[client_socket] = "left"
            elif len(self.clients_sockets) == 1:
                self.client_roles[client_socket] = "right"
            else:
                client_socket.close()
                continue  # Limite le jeu à deux clients

            self.clients_sockets.append(client_socket)
            print(f"Client {client_address} assigned role: {self.client_roles[client_socket]}")
            
            client_thread = ClientListener(self, client_socket, client_address)
            client_thread.start()

            if len(self.clients_sockets) > 1 and not self.ball_thread_started:
                self.ball_thread_running = True
                ball_thread = threading.Thread(target=self.sendBallPosition, daemon=True)
                ball_thread.start()
                self.ball_thread_started = True

    
    def remove_socket(self, socket):
        if socket in self.clients_sockets:
            self.clients_sockets.remove(socket)
    
    def sendBallPosition(self):
        while self.ball_thread_running:
            self.pos_ball = "BALL " + str(self.vitesse_balle_x) + " " + str(self.vitesse_balle_y) + " "
            for sock in self.clients_sockets:
                try:
                    sock.sendall(self.pos_ball.encode("UTF-8"))
                except socket.error:
                    print("Cannot send the message")
            time.sleep(10)  # Ajout d'une pause pour éviter la surcharge et permettre les autres actions

    def echo(self, data):
        
        print("Echoing:", data)
        if "BALL" in data:
            self.vitesse_balle_x = VITESSE_BALLE_X * random.choice([-1, 1])
            self.vitesse_balle_y = VITESSE_BALLE_Y * random.choice([-1, 1])
            self.pos_ball = "BALL " + str(self.vitesse_balle_x) + " " + str(self.vitesse_balle_y) + " "
            for sock in self.clients_sockets:
                try:
                    sock.sendall(self.pos_ball.encode("UTF-8"))
                except socket.error:
                    print("Cannot send the message")
        else :
            for sock in self.clients_sockets:
                try:
                    sock.sendall(data.encode("UTF-8"))
                except socket.error:
                    print("Cannot send the message")

if __name__ == "__main__":
    server = Server(59001)
    server.run()
