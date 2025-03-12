import tkinter as tk
import subprocess


def host_game():
    subprocess.Popen(['python', 'server.py'])


def join_game():
    subprocess.Popen(['python', 'client.py'])


root = tk.Tk()
root.title("Network Chess Menu")

label = tk.Label(root, text="Network Chess", font=("Helvetica", 24))
label.pack(pady=20)

host_button = tk.Button(root, text="Host Game", command=host_game)
host_button.pack(pady=10)

join_button = tk.Button(root, text="Join Game", command=join_game)
join_button.pack(pady=10)

root.mainloop()