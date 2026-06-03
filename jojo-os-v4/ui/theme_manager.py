# theme_manager.py
class Theme:
    # Cores JoJo (Padrão)
    JOJO = {
        "bg": "#000000",
        "fg": "#FFD700",  # Gold
        "accent": "#8A2BE2", # Purple
        "secondary": "#FF69B4", # Pink
        "display": "#1a1a1a"
    }
    
    # Cores Hacker (Cleitan-OS)
    HACKER = {
        "bg": "#0D0208", # Preto Matrix
        "fg": "#00FF41", # Verde Matrix
        "accent": "#008F11", # Verde Escuro
        "secondary": "#003B00", # Verde Musgo
        "display": "#000000"
    }

    current = HACKER # Começa como JoJo