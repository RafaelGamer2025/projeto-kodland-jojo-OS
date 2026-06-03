# matrix_animation.py
import tkinter as tk
import random

class MatrixFall:
    def __init__(self, window):
        self.window = window
        self.window.title("CLEITAN-OS // MATRIX_KERNEL")
        self.window.attributes("-fullscreen", True) # Abre em tela cheia para imersão
        self.window.configure(bg="black")

        # Configurações da animação
        self.width = self.window.winfo_screenwidth()
        self.height = self.window.winfo_screenheight()
        self.font_size = 18
        self.columns = int(self.width / self.font_size)
        
        # Cria o canvas (tela de desenho)
        self.canvas = tk.Canvas(window, width=self.width, height=self.height, bg="black", highlightthickness=0)
        self.canvas.pack()

        # Caracteres que vão cair (Mistura de Katakana e Números)
        self.chars = "ｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓﾔﾕﾖﾗﾘﾙﾚﾛﾜﾝ1234567890"
        self.drops = [0 for _ in range(self.columns)]

        # Atalho para sair: Pressione ESC para fechar a animação
        self.window.bind("<Escape>", lambda e: self.window.destroy())

        self.animate()

    def animate(self):
        # Cria um efeito de "rastro" desenhando um retângulo preto quase transparente sobre tudo
        self.canvas.create_rectangle(0, 0, self.width, self.height, fill="black", stipple="gray50", state="disabled")
        # Nota: O 'stipple' pode não funcionar em todos os sistemas, se ficar ruim, usamos um retângulo sólido
        self.canvas.create_rectangle(0, 0, self.width, self.height, fill="black", alpha=0.1) # Simulação

        # Limpa o rastro de forma simples para garantir compatibilidade
        self.canvas.create_rectangle(0, 0, self.width, self.height, fill="#000000", outline="", stipple="gray25")

        for i in range(len(self.drops)):
            char = random.choice(self.chars)
            x = i * self.font_size
            y = self.drops[i] * self.font_size

            # Desenha o caractere verde
            self.canvas.create_text(x, y, text=char, fill="#00FF00", font=("Courier", self.font_size, "bold"))

            # Reseta a gota se chegar no final da tela ou aleatoriamente
            if y > self.height and random.random() > 0.975:
                self.drops[i] = 0
            
            self.drops[i] += 1

        # Velocidade da animação (50ms = 20 FPS)
        self.window.after(50, self.animate)

def start_matrix():
    root = tk.Tk()
    MatrixFall(root)
    root.mainloop()

if __name__ == "__main__":
    start_matrix()