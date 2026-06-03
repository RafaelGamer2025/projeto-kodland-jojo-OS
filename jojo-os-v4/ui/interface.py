# interface.py
import tkinter as tk
from tkinter import scrolledtext
import threading
from ui.themes.jojo_theme import JoJoTheme
from core.ia_window import abrir_janela_ia

def iniciar_interface():
    root = tk.Tk()
    root.title("JOJO-OS 4.0 // BIZARRE ADVENTURE")
    root.geometry("900x600")
    root.configure(bg=JoJoTheme.BLACK)

    # ==========================
    # TERMINAL VISUAL (SPEEDWAGON FOUNDATION)
    # ==========================
    output = scrolledtext.ScrolledText(
        root,
        bg="#1A1A1A",
        fg=JoJoTheme.GOLD,
        font=("Courier New", 12, "bold"),
        insertbackground=JoJoTheme.GOLD
    )
    output.pack(fill="both", expand=True, padx=10, pady=10)

    # ==========================
    # LOG
    # ==========================
    def log(text):
        output.insert(tk.END, text + "\n")
        output.see(tk.END)

    # ==========================
    # BANNER
    # ==========================
    def show_banner():
        log("⭐ JOJO-OS 4.0: GOLDEN EXPERIENCE ⭐")
        log("SPEEDWAGON FOUNDATION KERNEL LOADED\n")
        log("WRYYYYYYYYYYYYYYYYYYYYYYY!\n")

    # ==========================
    # MENU
    # ==========================
    def show_menu():
        log("[1] HEAVEN'S DOOR (IA)")
        log("[2] HERMIT PURPLE (SCAN)")
        log("[3] D'ARBY'S GAMES")
        log("[4] SPEEDWAGON SCIENCE")
        log("[0] ARREVEDERCI (SAIR)\n")

    # ==========================
    # INPUT
    # ==========================
    frame = tk.Frame(root, bg=JoJoTheme.PURPLE)
    frame.pack(fill="x", side="bottom")

    entry = tk.Entry(
        frame,
        bg="#2A2A2A",
        fg=JoJoTheme.PINK,
        font=("Impact", 14),
        insertbackground=JoJoTheme.GOLD,
        bd=3,
        relief="sunken"
    )
    entry.pack(side="left", fill="x", expand=True, padx=10, pady=10)

    # ==========================
    # COMANDOS
    # ==========================
    def executar():
        cmd = entry.get()
        entry.delete(0, tk.END)

        log(f"⭐ {cmd}")

        if cmd == "1":
            abrir_janela_ia(root)

        elif cmd == "2":
            log("HERMIT PURPLE: Procurando Stands inimigos...")

        elif cmd == "3":
            log("D'ARBY: Good! Open the game!")

        elif cmd == "4":
            log("SPEEDWAGON: A ciência alemã é a melhor do mundo!")

        elif cmd == "0":
            root.destroy()

        else:
            log("MUDA MUDA MUDA! Comando inválido.")

    # botão executar
    tk.Button(
        frame,
        text="ORA!",
        bg=JoJoTheme.PURPLE,
        fg=JoJoTheme.GOLD,
        font=("Impact", 12, "bold"),
        command=executar,
        activebackground=JoJoTheme.PINK,
        activeforeground=JoJoTheme.WHITE
    ).pack(side="right", padx=10, pady=10)

    # ENTER executa
    entry.bind("<Return>", lambda e: executar())

    # iniciar
    show_banner()
    show_menu()

    root.mainloop()
