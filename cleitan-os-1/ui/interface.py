import tkinter as tk
from tkinter import scrolledtext
import threading

from core.ai import perguntar_ia
from ui.ia_window import abrir_janela_ia


def iniciar_interface():
    root = tk.Tk()
    root.title("CLEITAN OS 3.0")
    root.geometry("900x600")
    root.configure(bg="black")

    # ==========================
    # TERMINAL VISUAL
    # ==========================
    output = scrolledtext.ScrolledText(
        root,
        bg="black",
        fg="#00ff00",
        font=("Courier", 10)
    )
    output.pack(fill="both", expand=True)

    # ==========================
    # LOG (substitui console.print)
    # ==========================
    def log(text):
        output.insert(tk.END, text + "\n")
        output.see(tk.END)

    # ==========================
    # BANNER (substitui ASCII do rich)
    # ==========================
    def show_banner():
        log("=== CLEITAN OS 3.0 ===")
        log("Sistema iniciado com sucesso\n")

    # ==========================
    # MENU
    # ==========================
    def show_menu():
        log("[1] IA")
        log("[2] Port Scan")
        log("[3] Jogos")
        log("[4] Ciência")
        log("[0] Sair\n")

    # ==========================
    # INPUT
    # ==========================
    frame = tk.Frame(root, bg="black")
    frame.pack(fill="x")

    entry = tk.Entry(
        frame,
        bg="black",
        fg="#00ff00",
        insertbackground="#00ff00"
    )
    entry.pack(side="left", fill="x", expand=True)

    # ==========================
    # COMANDOS
    # ==========================
    def executar():
        cmd = entry.get()
        entry.delete(0, tk.END)

        log(f"> {cmd}")

        if cmd == "1":
            abrir_janela_ia(root)

        elif cmd == "2":
            log("Port scan em breve...")

        elif cmd == "3":
            log("Jogos em breve...")

        elif cmd == "4":
            log("Ciência em breve...")

        elif cmd == "0":
            root.destroy()

        else:
            log("Comando inválido")

    # botão executar
    tk.Button(
        frame,
        text="EXEC",
        bg="black",
        fg="#00ff00",
        command=executar
    ).pack(side="right")

    # ENTER executa
    entry.bind("<Return>", lambda e: executar())

    # iniciar
    show_banner()
    show_menu()

    root.mainloop()