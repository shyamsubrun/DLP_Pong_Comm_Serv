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
            # Déplacer la raquette droite, mais s'assurer qu'elle ne dépasse pas le bord supérieur (vide de 20px)
            if self.canvas.coords(self.right_paddle)[1] > 20:  
                self.canvas.move(self.right_paddle, 0, -22)
                self.client.send_data("MOVE RIGHT UP")
        elif event.keysym == "Down":
            # Déplacer la raquette droite, mais s'assurer qu'elle ne dépasse pas le bord inférieur (vide de 20px)
            if self.canvas.coords(self.right_paddle)[3] < 380:  # 400 (hauteur de l'écran) - 20 (vide)
                self.canvas.move(self.right_paddle, 0, 20)
                self.client.send_data("MOVE RIGHT DOWN")
        elif event.keysym == "w":
            # Déplacer la raquette gauche, mais s'assurer qu'elle ne dépasse pas le bord supérieur (vide de 20px)
            if self.canvas.coords(self.left_paddle)[1] > 20:  
                self.canvas.move(self.left_paddle, 0, -20)
                self.client.send_data("MOVE LEFT UP")
        elif event.keysym == "s":
            # Déplacer la raquette gauche, mais s'assurer qu'elle ne dépasse pas le bord inférieur (vide de 20px)
            if self.canvas.coords(self.left_paddle)[3] < 380:  # 400 (hauteur de l'écran) - 20 (vide)
                self.canvas.move(self.left_paddle, 0, 20)
                self.client.send_data("MOVE LEFT DOWN")

    def update_from_server(self, data):
        # Traiter les messages reçus du serveur pour mettre à jour l'état du jeu
        if data.startswith("MOVE LEFT UP"):
            if self.canvas.coords(self.left_paddle)[1] > 20:  # Vide de 20 pixels
                self.canvas.move(self.left_paddle, 0, -20)
        elif data.startswith("MOVE LEFT DOWN"):
            if self.canvas.coords(self.left_paddle)[3] < 380:  # Vide de 20 pixels
                self.canvas.move(self.left_paddle, 0, 20)
        elif data.startswith("MOVE RIGHT UP"):
            if self.canvas.coords(self.right_paddle)[1] > 20:  # Vide de 20 pixels
                self.canvas.move(self.right_paddle, 0, -20)
        elif data.startswith("MOVE RIGHT DOWN"):
            if self.canvas.coords(self.right_paddle)[3] < 380:  # Vide de 20 pixels
                self.canvas.move(self.right_paddle, 0, 20)
        elif data.startswith("BALL"):
            # Vérifie si le message est bien sous la forme "BALL x y"
            try:
                _, x, y = data.split()
                x, y = int(x), int(y)
                self.canvas.coords(self.ball, x-10, y-10, x+10, y+10)
            except ValueError:
                print("Erreur de format dans les données reçues :", data)

    def run_game(self):
        self.window.mainloop()
