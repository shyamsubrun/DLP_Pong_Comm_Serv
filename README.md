**Jeu Pong Multijoueur avec Connexion Client-Serveur - (2024-2025)**  
**Module** : Communication Réseau et Programmation Multithreadée - Projet Python Sockets
---
### Description
Ce projet a pour objectif de transformer un jeu Pong existant en une application multijoueur interactive en temps réel. En se basant sur une architecture client-serveur, cette application permet à plusieurs utilisateurs, connectés à travers un réseau local, de jouer ensemble. La mise en réseau repose sur des sockets TCP, avec une gestion de la synchronisation de la balle, des raquettes, et des scores en utilisant Python.

### Spécifications Techniques
- **Langage** : Python
- **Technologies de Communication** : 
  - **Sockets TCP** : Assurent la communication entre le serveur et les clients en temps réel.
  - **Multithreading** : Chaque client est géré par un thread distinct sur le serveur pour maintenir une interaction continue et fluide sans interruption.
- **Architecture** : 
  - **Client-Serveur** : Le serveur central gère la logique de jeu, notamment les mouvements de la balle, la détection des collisions, et la mise à jour des scores, tandis que les clients se chargent de l'affichage et des interactions de l'utilisateur.
- **Modélisation** : 
  - **Schéma d'Architecture** : Visualise l'interaction entre le serveur et plusieurs clients, mettant en évidence les flux de données (position de la balle, mouvements des raquettes, score).
  - **Diagramme de Séquence** : Décrit les étapes des échanges de données entre client et serveur pour chaque action (connexion, déconnexion, mouvement, collision).

### Fonctionnalités de Mise en Réseau
- **Connexion Multijoueur en Réseau** : Les utilisateurs peuvent se connecter à un serveur central, ce qui leur permet de jouer ensemble sur des ordinateurs distincts, en partageant la même session de jeu.
- **Synchronisation des Mouvements et de la Balle** : Le serveur diffuse continuellement la position de la balle et les mouvements des raquettes, garantissant une synchronisation en temps réel pour tous les joueurs.
- **Détection de Collisions en Temps Réel** : Le serveur détecte et gère les collisions entre la balle et les raquettes, simulant un rebond de la balle pour une expérience de jeu réaliste.
- **Gestion des Scores Partagés** : Le serveur suit les scores des joueurs et les diffuse à chaque client lorsqu’un point est marqué, permettant aux utilisateurs de voir le score mis à jour en temps réel.
- **Déconnexion Sécurisée et Gestion des Erreurs Réseau** : En cas de déconnexion d’un joueur, le serveur ajuste les connexions restantes et gère la fermeture de la session de jeu.

### Structure de Données
- **Données Transmises** :
  - **Position de la Balle** : Coordonnées X et Y, diffusées par le serveur pour synchroniser l’affichage entre tous les clients.
  - **Positions des Raquettes** : Coordonnées de la raquette gauche et droite, envoyées par les clients et répercutées par le serveur aux autres joueurs.
  - **Scores** : Maintien des scores pour chaque joueur, mis à jour en temps réel dès qu’un point est marqué.

### Remarques
- **Objectif de la Connexion Réseau** : Transformer le jeu Pong en une expérience multijoueur interactive en utilisant une architecture réseau avec des sockets TCP, tout en garantissant la réactivité de l’expérience de jeu.
- **Documentation et Modélisation** : 
  - **Schéma d'Architecture** : Illustrant le flux de communication entre clients et serveur pour la gestion en temps réel des positions de la balle et des raquettes.
  - **Diagramme de Séquence** : Détaillant les étapes d’interaction entre client et serveur pour chaque action importante (connexion, mouvement, rebond).
- **Tests de Performance et Résilience** : Tests en conditions réelles pour évaluer la performance de la communication réseau et vérifier la fluidité de la synchronisation des actions multijoueurs.

### Code du Projet
Le projet comprend trois composants principaux :
1. **Client (`PongClient`)** : Se connecte au serveur, envoie les actions du joueur (mouvements de raquette), reçoit les mises à jour en temps réel (positions de la balle et des raquettes), et gère l’interface graphique du jeu.
2. **Logique du Jeu (`PongGame`)** : Responsable de l'affichage de la balle, des raquettes et des scores ; se met à jour en fonction des données reçues du serveur.
3. **Serveur (`PongServer`)** : Gère la logique centrale du jeu, incluant les mises à jour de la balle, la détection de collision, la gestion des scores et la diffusion des données à tous les clients connectés via un système de sockets multithreadé.
