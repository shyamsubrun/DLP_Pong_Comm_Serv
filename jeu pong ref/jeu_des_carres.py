import tkinter as tk
import random

# Dimensions de la fenêtre
LARGEUR = 600
HAUTEUR = 400

# Dimensions des raquettes
LARGEUR_RAQUETTE = 10
HAUTEUR_RAQUETTE = 100

# Vitesse de déplacement des raquettes
VITESSE_RAQUETTE = 20

# Vitesse initiale de la balle
VITESSE_BALLE_X = 5
VITESSE_BALLE_Y = 5

class PongGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Jeu de Pong")
        self.canvas = tk.Canvas(self.master, width=LARGEUR, height=HAUTEUR, bg="black")
        self.canvas.pack()

        # Initialisation des raquettes
        self.raquette_gauche = self.canvas.create_rectangle(
            10, HAUTEUR//2 - HAUTEUR_RAQUETTE//2,
            10 + LARGEUR_RAQUETTE, HAUTEUR//2 + HAUTEUR_RAQUETTE//2,
            fill="white"
        )
        self.raquette_droite = self.canvas.create_rectangle(
            LARGEUR - 10 - LARGEUR_RAQUETTE, HAUTEUR//2 - HAUTEUR_RAQUETTE//2,
            LARGEUR - 10, HAUTEUR//2 + HAUTEUR_RAQUETTE//2,
            fill="white"
        )

        # Initialisation de la balle
        self.balle = self.canvas.create_oval(
            LARGEUR//2 - 10, HAUTEUR//2 - 10,
            LARGEUR//2 + 10, HAUTEUR//2 + 10,
            fill="white"
        )
        self.vitesse_balle_x = VITESSE_BALLE_X * random.choice([-1, 1])
        self.vitesse_balle_y = VITESSE_BALLE_Y * random.choice([-1, 1])

        # Scores
        self.score_gauche = 0
        self.score_droite = 0
        self.affichage_score = self.canvas.create_text(
            LARGEUR//2, 20,
            text=f"{self.score_gauche}   {self.score_droite}",
            font=("Arial", 24),
            fill="white"
        )

        # Bind des touches
        self.master.bind("<KeyPress>", self.mouvement_raquette)
        self.master.bind("<KeyRelease>", self.stop_raquette)

        # Dictionnaire pour suivre les touches pressées
        self.touches = {
            "z": False,
            "s": False,
            "Up": False,
            "Down": False
        }

        # Démarrer le jeu
        self.jeu_en_cours = True
        self.mouvement()

    def mouvement_raquette(self, event):
        if event.keysym in self.touches:
            self.touches[event.keysym] = True

    def stop_raquette(self, event):
        if event.keysym in self.touches:
            self.touches[event.keysym] = False

    def mouvement(self):
        if self.jeu_en_cours:
            # Déplacement des raquettes
            if self.touches["z"]:
                self.deplacer_raquette(self.raquette_gauche, -VITESSE_RAQUETTE)
            if self.touches["s"]:
                self.deplacer_raquette(self.raquette_gauche, VITESSE_RAQUETTE)
            if self.touches["Up"]:
                self.deplacer_raquette(self.raquette_droite, -VITESSE_RAQUETTE)
            if self.touches["Down"]:
                self.deplacer_raquette(self.raquette_droite, VITESSE_RAQUETTE)

            # Déplacement de la balle
            self.canvas.move(self.balle, self.vitesse_balle_x, self.vitesse_balle_y)
            pos_balle = self.canvas.coords(self.balle)

            # Collision avec le haut ou le bas
            if pos_balle[1] <= 0 or pos_balle[3] >= HAUTEUR:
                self.vitesse_balle_y = -self.vitesse_balle_y

            # Collision avec les raquettes
            if self.collision(self.raquette_gauche, pos_balle):
                self.vitesse_balle_x = abs(self.vitesse_balle_x)
            elif self.collision(self.raquette_droite, pos_balle):
                self.vitesse_balle_x = -abs(self.vitesse_balle_x)

            # Sortie de la balle à gauche ou à droite
            if pos_balle[0] <= 0:
                self.score_droite += 1
                self.mise_a_jour_score()
                self.reinitialiser_balle()
            elif pos_balle[2] >= LARGEUR:
                self.score_gauche += 1
                self.mise_a_jour_score()
                self.reinitialiser_balle()

            self.master.after(30, self.mouvement)

    def deplacer_raquette(self, raquette, dy):
        pos = self.canvas.coords(raquette)
        if pos[1] + dy >= 0 and pos[3] + dy <= HAUTEUR:
            self.canvas.move(raquette, 0, dy)

    def collision(self, raquette, pos_balle):
        pos_raquette = self.canvas.coords(raquette)
        return (
            pos_raquette[0] < pos_balle[2] and
            pos_raquette[2] > pos_balle[0] and
            pos_raquette[1] < pos_balle[3] and
            pos_raquette[3] > pos_balle[1]
        )

    def mise_a_jour_score(self):
        self.canvas.itemconfig(self.affichage_score, text=f"{self.score_gauche}   {self.score_droite}")
        if self.score_gauche == 3 or self.score_droite == 3:
            self.jeu_en_cours = False
            self.canvas.create_text(
                LARGEUR//2, HAUTEUR//2,
                text="Fin du jeu",
                font=("Arial", 24),
                fill="white"
            )

    def reinitialiser_balle(self):
        self.canvas.coords(
            self.balle,
            LARGEUR//2 - 10, HAUTEUR//2 - 10,
            LARGEUR//2 + 10, HAUTEUR//2 + 10
        )
        self.vitesse_balle_x = VITESSE_BALLE_X * random.choice([-1, 1])
        self.vitesse_balle_y = VITESSE_BALLE_Y * random.choice([-1, 1])

if __name__ == "__main__":
    root = tk.Tk()
    jeu = PongGame(root)
    root.mainloop()
