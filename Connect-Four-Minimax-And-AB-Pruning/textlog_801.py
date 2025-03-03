# UNC Charlotte 
# ITCS 5153 - Applied AI - Spring 2025 
# Lab 3 
# Adversarial Search / Game Playing 
# This module implements the game log
# Student ID: 801


import tkinter as tk
from tkinter.scrolledtext import ScrolledText


# Creating game log to keep track of moves
class LogGUI():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Game Log")
        self.root.geometry("800x300")

        # Creates scroll
        self.text_area = ScrolledText(self.root, wrap=tk.WORD, font=("Arial", 12))
        self.text_area.pack(expand=True, fill="both")
        self.text_area.config(state=tk.DISABLED)

    # Add a message to the log
    def add_log(self, message):
        self.text_area.config(state=tk.NORMAL)
        self.text_area.insert(tk.END, message + "\n")
        self.text_area.config(state=tk.DISABLED)
        self.text_area.yview(tk.END)

    # Update the visuals
    def update(self):
        self.root.update_idletasks()
        self.root.update()

    # Run the visuals
    def run(self):
        self.root.mainloop()

