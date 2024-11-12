import socket
import threading
import tkinter as tk

LARGEUR = 600
HAUTEUR = 400

class PongClient:
    def __init__(self, username, server, port):
        self.username = username
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((server, port))
        self.init_ui()
        self.listening = True
        self.listen_thread = threading.Thread(target=self.receive_data)
        self.listen_thread.start()

    def init_ui(self):
        self.root = tk.Tk()
        self.root.title(f"Pong - {self.username}")
        self.canvas = tk.Canvas(self.root, width=LARGEUR, height=HAUTEUR, bg="black")
        self.canvas.pack()

        # Raquettes
        self.raquette = self.canvas.create_rectangle(
            10, HAUTEUR // 2 - 50, 20, HAUTEUR // 2 + 50, fill="white"
        )
        self.opponent_raquette = self.canvas.create_rectangle(
            LARGEUR - 20, HAUTEUR // 2 - 50, LARGEUR - 10, HAUTEUR // 2 + 50, fill="white"
        )

        # Balle
        self.balle = self.canvas.create_oval(
            LARGEUR // 2 - 10, HAUTEUR // 2 - 10, LARGEUR // 2 + 10, HAUTEUR // 2 + 10, fill="white"
        )

        self.canvas.bind_all("<KeyPress-Up>", lambda e: self.move_paddle(-10))
        self.canvas.bind_all("<KeyPress-Down>", lambda e: self.move_paddle(10))

        self.root.after(30, self.update_ui)
        self.root.mainloop()

    def move_paddle(self, dy):
        self.canvas.move(self.raquette, 0, dy)
        pos = self.canvas.coords(self.raquette)
        data = f"MOVE_PADDLE {pos[1]} {pos[3]}"
        self.send(data)

    def update_ui(self):
        # Mettre à jour les éléments du jeu en fonction des données reçues
        self.root.after(30, self.update_ui)

    def receive_data(self):
        while self.listening:
            try:
                data = self.socket.recv(1024).decode('UTF-8')
                if data:
                    self.handle_server_data(data)
            except socket.error:
                print("Disconnected from server.")
                self.listening = False

    def handle_server_data(self, data):
        parts = data.split()
        if parts[0] == "BALL":
            x, y = float(parts[1]), float(parts[2])
            self.canvas.coords(self.balle, x - 10, y - 10, x + 10, y + 10)

    def send(self, data):
        try:
            self.socket.sendall(data.encode('UTF-8'))
        except socket.error:
            print("Failed to send data.")

if __name__ == "__main__":
    username = input("Enter username: ")
    server = input("Enter server IP: ")
    port = int(input("Enter port: "))
    PongClient(username, server, port)
