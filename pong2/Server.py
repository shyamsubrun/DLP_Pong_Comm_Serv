import socket
import signal #identifie les signaux pour kill le programme
import sys #utilisé pour sortir du programme
import time
import threading
from ClientThread import ClientListener
import random
VITESSE_BALLE_X = 5
VITESSE_BALLE_Y = 5
class Server():
    vitesse_balle_x = VITESSE_BALLE_X * random.choice([-1, 1])
    vitesse_balle_y = VITESSE_BALLE_Y * random.choice([-1, 1])
    pos_ball = "BALL"+" "+str(vitesse_balle_x) +" "+ str(vitesse_balle_y)+ " "
    
    def __init__(self, port):
        self.listener= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listener.bind(('', port))
        self.listener.listen(1)
        print("Listening on port", port)
        self.clients_sockets= []

    def run(self):
        while True:
            print("listening new customers")
            try:
                (client_socket, client_adress) = self.listener.accept()
            except socket.error:
                sys.exit("Cannot connect clients")
            self.clients_sockets.append(client_socket)
            print("Start the thread for client:", client_adress)
            client_thread= ClientListener(self, client_socket, client_adress)
            client_thread.start()
            time.sleep(0.1)
            if len(self.clients_sockets)>1 : 
                print("test from ball thread")
                ball_thread = threading.Thread(target=self.sendBallPosition)
                ball_thread.start()
            

    def remove_socket(self, socket):
        self.client_sockets.remove(socket)


    def sendBallPosition(self):
        while True:
            for sock in self.clients_sockets:
                try:
                    sock.sendall(self.pos_ball.encode("UTF-8"))
                except socket.error:
                    print("Cannot send the message")
        
    def echo(self, data):
        print("echoing:", data)
        print(self.pos_ball)
        for sock in self.clients_sockets:
            try:
                sock.sendall(data.encode("UTF-8"))
            except socket.error:
                print("Cannot send the message")




if __name__ == "__main__":
    server= Server(59001)
    server.run()