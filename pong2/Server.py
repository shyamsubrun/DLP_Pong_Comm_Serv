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
        self.j1 = 0
        self.j2 = 0
        self.joueurs = []
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
            client_thread = ClientListener(self, client_socket, client_address)
            client_thread.start()
            if len(self.clients_sockets) > 1 and not self.ball_thread_started:
                time.sleep(3)
                self.ball_thread_running = True
                print("Starting the ball movement thread")
                ball_thread = threading.Thread(target=self.sendBallPosition, daemon=True)
                ball_thread.start()
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
        parts_data = data.split(" ")
        print(parts_data)
        last_word = parts_data[-1] if parts_data else ""
        print("Echoing:", data)
        if "joined" in data : 
            self.joueurs.append(data.split(" ")[0])
        if "BALL" in data:
            self.vitesse_balle_x = VITESSE_BALLE_X * random.choice([-1, 1])
            self.vitesse_balle_y = VITESSE_BALLE_Y * random.choice([-1, 1])
            self.pos_ball = "BALL " + str(self.vitesse_balle_x) + " " + str(self.vitesse_balle_y) + " "
            if parts_data[2] == "1" :
                self.j1+=1
            elif parts_data[2] == "2" :
                self.j2+=1
            self.put_joueur = "PUT " + str(self.j1) +  " " + str(self.j2)+ " "
            for sock in self.clients_sockets:
                try:
                    sock.sendall(self.pos_ball.encode("UTF-8"))
                    sock.sendall(self.put_joueur.encode("UTF-8"))
                except socket.error:
                    print("Cannot send the message")
        else :
            
            if len(self.joueurs) > 0 and self.joueurs[0] in data and last_word in ["z", "s"]:
                return
            if len(self.joueurs) > 1 and self.joueurs[1] in data and last_word in ["Up", "Down"]:
                return
            else :
                for sock in self.clients_sockets:
                    try:
                        sock.sendall(data.encode("UTF-8"))
                    except socket.error:
                        print("Cannot send the message")

if __name__ == "__main__":
    server = Server(59001)
    server.run()
