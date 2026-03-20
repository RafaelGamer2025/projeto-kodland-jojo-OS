import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os

# Importando seus módulos
from core.calc_window import HackerCalc
from ui.mod_menu import ModMenu  # Importando o novo módulo de menu

class CleitanOS:
    def __init__(self, root):
        self.root = root
        self.root.title("CLEITAN-OS v3.0")
        self.root.geometry("1000x700")
        self.root.configure(bg="#0a0a0a")  # Fundo preto

        # --- BARRA DE TAREFAS (Estilo Windows/Chrome) ---
        self.taskbar = tk.Frame(root, bg="#1a1a1a", height=40)
        self.taskbar.pack(side="bottom", fill="x")

        # --- ÁREA DE TRABALHO ---
        self.desktop = tk.Canvas(root, bg="#0a0a0a", highlightthickness=0)
        self.desktop.pack(expand=True, fill="both")

        # Adicionando Ícones na Área de Trabalho
        self.add_app_icon("Calculadora", "🧮", self.open_calc, 40, 40)
        self.add_app_icon("Gemini IA", "🤖", self.open_ai, 40, 140)
        self.add_app_icon("Antivírus", "🛡️", self.open_antivirus, 40, 240)
        self.add_app_icon("Jogo", "🎮", self.open_game, 40, 340)  # Ícone do jogo
        self.add_app_icon("Navegador", "🌐", self.open_browser, 40, 440)  # Ícone do navegador

        # Relógio na barra de tarefas
        self.clock_label = tk.Label(self.taskbar, text="", fg="#00ff00", bg="#1a1a1a", font=("Courier", 10))
        self.clock_label.pack(side="right", padx=10)
        self.update_time()

        # Inicializando o menu flutuante
        self.mod_menu = ModMenu(self.root)

    def add_app_icon(self, name, icon, command, x, y):
        """Cria um ícone que abre janelas"""
        btn = tk.Button(self.root, text=f"{icon}\n{name}", command=command,
                        bg="#0a0a0a", fg="#00ff00", font=("Courier", 10, "bold"),
                        bd=0, activebackground="#1a1a1a", activeforeground="#00ff00",
                        padx=10, pady=10)
        btn.place(x=x, y=y)

    def open_calc(self):
        calc_window = tk.Toplevel(self.root)
        HackerCalc(calc_window)

    def open_ai(self):
        messagebox.showinfo("Cleitan-OS", "Iniciando Interface do Gemini...")

    def open_antivirus(self):
        messagebox.showinfo("Segurança", "Módulo Antivírus em Janela carregando...")

    def open_game(self):
        os.system('python games/pygame_game/main.py')  # Executa o jogo

    def open_browser(self):
        messagebox.showinfo("Navegador", "Abrindo o navegador estilo hacker...")

    def update_time(self):
        import time
        self.clock_label.config(text=time.strftime("%H:%M:%S"))
        self.root.after(1000, self.update_time)

if __name__ == "__main__":
    root = tk.Tk()
    app = CleitanOS(root)
    root.mainloop()