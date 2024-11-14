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
        self.ball_thread_started = False  # Pour s'assurer qu'on ne crée qu'un seul thread pour la balle
        self.ball_thread_running = True
    def run(self):
        print("test from run")
        while True:
            print("Listening for new clients...")
            try:
                (client_socket, client_address) = self.listener.accept()
            except socket.error:
                sys.exit("Cannot connect clients")
                
            self.clients_sockets.append(client_socket)
            print("Start the thread for client:", client_address)
            
            if len(self.clients_sockets) > 1 and not self.ball_thread_started:
                self.ball_thread_running = True
                print("Starting the ball movement thread")
                ball_thread = threading.Thread(target=self.sendBallPosition, daemon=True)
                ball_thread.start()
                client_thread = ClientListener(self, client_socket, client_address)
                client_thread.start()
                time.sleep(0.1)
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
            time.sleep(200)  # Ajout d'une pause pour éviter la surcharge et permettre les autres actions

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
