import socket
import threading
import time
import re
import tkinter as tk

class PongClient:
    def __init__(self, username, server, port):
        self.username = username
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((server, port))
        self.send(f"USERNAME {username}")
        self.listening = True
        self.init_ui()
        self.listen_thread = threading.Thread(target=self.listener)
        self.listen_thread.start()

    def init_ui(self):
        self.root = tk.Tk()
        self.root.title(f"Pong Game - {self.username}")
        self.canvas = tk.Canvas(self.root, width=600, height=400, bg="black")
        self.canvas.pack()
        self.paddle = self.canvas.create_rectangle(50, 150, 60, 250, fill="white")
        self.ball = self.canvas.create_oval(290, 190, 310, 210, fill="white")
        self.canvas.bind_all("<KeyPress-Up>", lambda e: self.move_paddle(-10))
        self.canvas.bind_all("<KeyPress-Down>", lambda e: self.move_paddle(10))
        self.root.after(30, self.update)
        self.root.mainloop()

    def move_paddle(self, delta_y):
        self.canvas.move(self.paddle, 0, delta_y)
        pos = self.canvas.coords(self.paddle)
        self.send(f"MOVE_PADDLE {pos}")

    def update(self):
        self.canvas.move(self.ball, 5, 5)
        pos = self.canvas.coords(self.ball)
        self.send(f"MOVE_BALL {pos}")
        self.root.after(30, self.update)

    def listener(self):
        while self.listening:
            data = ""
            try:
                data = self.socket.recv(1024).decode('UTF-8')
                if data:
                    self.handle_msg(data)
            except socket.error:
                print("Unable to receive data")
                self.listening = False
            time.sleep(0.1)

    def send(self, message):
        try:
            if not re.match('^USERNAME', message):
                message = f"{self.username}: {message}"
            self.socket.sendall(message.encode("UTF-8"))
        except socket.error:
            print("Unable to send message")

    def handle_msg(self, data):
        print(f"Received: {data}")
        if data == "QUIT":
            self.listening = False
        else:
            parts = data.split()
            if parts[0] == "MOVE_PADDLE":
                x1, y1, x2, y2 = map(int, parts[1:])
                self.canvas.coords(self.paddle, x1, y1, x2, y2)
            elif parts[0] == "MOVE_BALL":
                x1, y1, x2, y2 = map(int, parts[1:])
                self.canvas.coords(self.ball, x1, y1, x2, y2)

if __name__ == "__main__":
    username = input("Enter username: ")
    server = input("Enter server address: ")
    port = int(input("Enter server port: "))
    client = PongClient(username, server, port)
