import tkinter as tk
from tkinter import Menu

class ModMenu:
    def __init__(self, master):
        self.master = master
        self.menu = Menu(master)
        master.config(menu=self.menu)

        # Criando o menu flutuante
        self.app_menu = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Aplicativos", menu=self.app_menu)
        
        # Adicionando opções ao menu
        self.app_menu.add_command(label="Calculadora", command=self.open_calc)
        self.app_menu.add_command(label="Gemini IA", command=self.open_ai)
        self.app_menu.add_command(label="Antivírus", command=self.open_antivirus)
        self.app_menu.add_command(label="Jogo", command=self.open_game)
        self.app_menu.add_command(label="Navegador", command=self.open_browser)

    def open_calc(self):
        # Lógica para abrir a calculadora
        pass

    def open_ai(self):
        # Lógica para abrir a interface da IA
        pass

    def open_antivirus(self):
        # Lógica para abrir o módulo antivírus
        pass

    def open_game(self):
        # Lógica para abrir o jogo
        pass

    def open_browser(self):
        # Lógica para abrir o navegador
        pass

def create_mod_menu(root):
    ModMenu(root)