import tkinter as tk
import subprocess


def start_local_game():
    subprocess.Popen(['python', 'main.py'])


def start_network_game():
    subprocess.Popen(['python', 'network_menu.py'])


root = tk.Tk()
root.title("Chess Menu")
root.geometry('800x600')

label = tk.Label(root, text="CHESS", font=("Helvetica", 24))
label.pack(pady=20)

play_local_button = tk.Button(root, text="Play on one PC", command=start_local_game)
play_local_button.pack(pady=10)

play_network_button = tk.Button(root, text="Play on two PCs", command=start_network_game)
play_network_button.pack(pady=10)

play_with_computer_button = tk.Button(root, text="Play with computer (not implemented yet)")
play_with_computer_button.pack(pady=10)

root.mainloop()