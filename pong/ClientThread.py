import tkinter as tk

class PongGame:
    def __init__(self, client):
        self.client = client
        self.window = tk.Tk()
        self.window.title("Pong")
        self.canvas = tk.Canvas(self.window, width=600, height=400, bg="black")
        self.canvas.pack()

        # Initialiser les éléments du jeu
        self.ball = self.canvas.create_oval(290, 190, 310, 210, fill="white")
        self.left_paddle = self.canvas.create_rectangle(10, 150, 20, 250, fill="white")
        self.right_paddle = self.canvas.create_rectangle(580, 150, 590, 250, fill="white")
        
        # Lancer la mise à jour graphique et les contrôles
        self.window.bind("<KeyPress>", self.move_paddle)

    def move_paddle(self, event):
        if event.keysym == "Up":
            self.canvas.move(self.right_paddle, 0, -20)
            self.client.send_data("MOVE RIGHT UP")
        elif event.keysym == "Down":
            self.canvas.move(self.right_paddle, 0, 20)
            self.client.send_data("MOVE RIGHT DOWN")
        elif event.keysym == "w":
            self.canvas.move(self.left_paddle, 0, -20)
            self.client.send_data("MOVE LEFT UP")
        elif event.keysym == "s":
            self.canvas.move(self.left_paddle, 0, 20)
            self.client.send_data("MOVE LEFT DOWN")

    def update_from_server(self, data):
        # Traiter les messages reçus du serveur pour mettre à jour l'état du jeu
        if "MOVE LEFT UP" in data:
            self.canvas.move(self.left_paddle, 0, -20)
        elif "MOVE LEFT DOWN" in data:
            self.canvas.move(self.left_paddle, 0, 20)
        elif "MOVE RIGHT UP" in data:
            self.canvas.move(self.right_paddle, 0, -20)
        elif "MOVE RIGHT DOWN" in data:
            self.canvas.move(self.right_paddle, 0, 20)
        elif "BALL" in data:
            # Mettre à jour la position de la balle
            _, x, y = data.split()
            x, y = int(x), int(y)
            self.canvas.coords(self.ball, x-10, y-10, x+10, y+10)

    def run_game(self):
        self.window.mainloop()
