# jojo_theme.py
import tkinter as tk

class JoJoTheme:
    # Cores icônicas de JoJo
    PURPLE = "#6A0DAD"  # Roxo profundo (Star Platinum / Dio)
    GOLD = "#FFD700"    # Ouro (The World / Golden Experience)
    PINK = "#FF69B4"    # Rosa choque (Logo / Estilo)
    BLACK = "#000000"
    WHITE = "#FFFFFF"
    
    def __init__(self, root):
        self.root = root
        self.apply_theme()

    def apply_theme(self):
        """Aplica o tema JoJo à interface"""
        self.root.configure(bg=self.BLACK)
        self.root.option_add("*Font", "Impact 12")  # Fonte mais impactante
        self.root.option_add("*Foreground", self.GOLD)
        self.root.option_add("*Background", self.PURPLE)
        self.root.option_add("*HighlightBackground", self.PINK)
        self.root.option_add("*HighlightColor", self.GOLD)

    @staticmethod
    def get_button_style():
        return {
            "bg": "#6A0DAD",
            "fg": "#FFD700",
            "activebackground": "#FF69B4",
            "activeforeground": "#FFFFFF",
            "font": ("Impact", 12),
            "bd": 2,
            "relief": "raised"
        }

    @staticmethod
    def get_entry_style():
        return {
            "bg": "#1A1A1A",
            "fg": "#FF69B4",
            "insertbackground": "#FFD700",
            "font": ("Courier New", 12, "bold")
        }
