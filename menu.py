import tkinter as tk
import subprocess


def start_game():
    subprocess.Popen(['python', 'main.py'])


root = tk.Tk()
root.title("Chess Menu")

label = tk.Label(root, text="CHESS", font=("Helvetica", 24))
label.pack(pady=20)

play_with_player_button = tk.Button(root, text="Play with another player", command=start_game)
play_with_player_button.pack(pady=10)

play_with_computer_button = tk.Button(root, text="Play with computer (not implemented yet)")
play_with_computer_button.pack(pady=10)

root.mainloop()
# TEST
