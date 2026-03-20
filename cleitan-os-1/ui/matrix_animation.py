import tkinter as tk
import random

class MatrixAnimation:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, bg="black", width=800, height=600)
        self.canvas.pack()
        self.columns = 80
        self.drops = [0] * self.columns
        self.font_size = 20
        self.characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        self.animate()

    def animate(self):
        self.canvas.delete("all")
        for i in range(len(self.drops)):
            char = random.choice(self.characters)
            x = i * self.font_size
            y = self.drops[i] * self.font_size
            self.canvas.create_text(x, y, text=char, fill="green", font=("Courier", self.font_size))
            if self.drops[i] * self.font_size > self.canvas.winfo_height() and random.random() > 0.975:
                self.drops[i] = 0
            self.drops[i] += 1
        self.root.after(100, self.animate)

if __name__ == "__main__":
    root = tk.Tk()
    app = MatrixAnimation(root)
    root.mainloop()