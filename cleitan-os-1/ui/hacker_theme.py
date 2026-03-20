# filepath: c:\Users\Rafael\OneDrive\Anexos\Área de Trabalho\site\cleitan-os\ui\hacker_theme.py
import tkinter as tk

class HackerTheme:
    def __init__(self, root):
        self.root = root
        self.apply_theme()

    def apply_theme(self):
        """Aplica o tema hacker à interface"""
        self.root.configure(bg="#0a0a0a")  # Fundo preto
        self.root.option_add("*Font", "Courier 10")  # Fonte padrão
        self.root.option_add("*Foreground", "#00ff00")  # Texto verde
        self.root.option_add("*Background", "#1a1a1a")  # Fundo cinza escuro
        self.root.option_add("*HighlightBackground", "#1a1a1a")  # Fundo de destaque
        self.root.option_add("*HighlightColor", "#00ff00")  # Cor de destaque verde

    def create_button(self, text, command):
        """Cria um botão estilizado"""
        return tk.Button(self.root, text=text, command=command,
                         bg="#0a0a0a", fg="#00ff00", bd=0,
                         activebackground="#1a1a1a", activeforeground="#00ff00",
                         padx=10, pady=5)

    def create_label(self, text):
        """Cria um rótulo estilizado"""
        return tk.Label(self.root, text=text, bg="#0a0a0a", fg="#00ff00")