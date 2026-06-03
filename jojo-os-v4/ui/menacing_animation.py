# menacing_animation.py
import tkinter as tk
import random

class MenacingFall:
    def __init__(self, window):
        self.window = window
        self.window.title("JOJO-OS // MENACING_KERNEL")
        self.window.attributes("-fullscreen", True)
        self.window.configure(bg="black")

        self.width = self.window.winfo_screenwidth()
        self.height = self.window.winfo_screenheight()
        self.font_size = 24
        self.columns = int(self.width / (self.font_size * 2))
        
        self.canvas = tk.Canvas(window, width=self.width, height=self.height, bg="black", highlightthickness=0)
        self.canvas.pack()

        # Onomatopeia clássica de JoJo: ゴゴゴゴ (Gogogogo)
        self.chars = ["ゴ", "ゴ", "ゴ", "ゴ", "MENACING", "ドドド", "DIO!"]
        self.drops = [random.randint(-20, 0) for _ in range(self.columns)]
        self.colors = ["#6A0DAD", "#FFD700", "#FF69B4", "#FFFFFF"]

        self.window.bind("<Escape>", lambda e: self.window.destroy())
        self.animate()

    def animate(self):
        # Efeito de rastro
        self.canvas.create_rectangle(0, 0, self.width, self.height, fill="black", stipple="gray25")
        
        # Limpeza simples para compatibilidade
        self.canvas.delete("all")
        self.canvas.create_rectangle(0, 0, self.width, self.height, fill="black")

        for i in range(len(self.drops)):
            char = random.choice(self.chars)
            color = random.choice(self.colors)
            x = i * (self.font_size * 2)
            y = self.drops[i] * self.font_size

            # Desenha o caractere com estilo JoJo
            self.canvas.create_text(x, y, text=char, fill=color, font=("Impact", self.font_size, "bold"))

            if y > self.height and random.random() > 0.95:
                self.drops[i] = 0
            
            self.drops[i] += 1

        self.window.after(60, self.animate)

def start_menacing():
    root = tk.Tk()
    MenacingFall(root)
    root.mainloop()

if __name__ == "__main__":
    start_menacing()
