import tkinter as tk
from tkinter import scrolledtext
import threading

from core.ai import perguntar_ia  # função da IA

def abrir_janela_ia(root):
    janela = tk.Toplevel(root)
    janela.title("CLEITAN IA SYSTEM")
    janela.geometry("700x500")
    janela.configure(bg="black")

    # sempre na frente
    janela.attributes("-topmost", True)

    # ==========================
    # ÁREA DE CHAT
    # ==========================
    chat = scrolledtext.ScrolledText(
        janela,
        bg="black",
        fg="#00ff00",
        font=("Courier", 10)
    )
    chat.pack(fill="both", expand=True)

    # ==========================
    # INPUT
    # ==========================
    frame = tk.Frame(janela, bg="black")
    frame.pack(fill="x")

    entry = tk.Entry(
        frame,
        bg="black",
        fg="#00ff00",
        insertbackground="#00ff00"
    )
    entry.pack(side="left", fill="x", expand=True)

    # ==========================
    # FUNÇÃO DE LOG
    # ==========================
    def log(text):
        chat.insert(tk.END, text + "\n")
        chat.see(tk.END)

    # ==========================
    # ENVIAR PERGUNTA
    # ==========================
    def enviar():
        pergunta = entry.get()
        entry.delete(0, tk.END)

        log(f"> {pergunta}")

        def run():
            try:
                resposta = perguntar_ia(pergunta)
                log("[IA]")
                log(resposta)
            except Exception as e:
                log(f"[ERRO] {e}")

        threading.Thread(target=run, daemon=True).start()

    # botão
    btn = tk.Button(
        frame,
        text="ENVIAR",
        bg="black",
        fg="#00ff00",
        command=enviar
    )
    btn.pack(side="right")

    # ENTER envia
    entry.bind("<Return>", lambda e: enviar())