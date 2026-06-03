import tkinter as tk
import subprocess
import os




class TerminalWindow:

    def __init__(self, master):

        self.win = tk.Toplevel(master)

        self.win.title("💻 JOJO TERMINAL")

        self.win.geometry("900x500")

        self.win.configure(bg="black")

        # ===== OUTPUT =====

        self.output = tk.Text(
            self.win,
            bg="black",
            fg="lime",
            insertbackground="lime",
            font=("Consolas", 11)
        )

        self.output.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        # ===== INPUT =====

        self.entry = tk.Entry(
            self.win,
            bg="#111",
            fg="lime",
            insertbackground="lime",
            font=("Consolas", 12)
        )

        self.entry.pack(
            fill="x",
            padx=10,
            pady=10
        )

        self.entry.bind(
            "<Return>",
            self.executar
        )

        self.escrever(
            "JOJO-OS TERMINAL ONLINE...\n"
        )

    # ======================================================
    # ESCREVER
    # ======================================================

    def escrever(self, texto):

        self.output.insert(
            "end",
            texto
        )

        self.output.see("end")

    # ======================================================
    # EXECUTAR
    # ======================================================

    def executar(self, event=None):

        comando = self.entry.get()

        self.escrever(
            f"\n> {comando}\n"
        )

        self.entry.delete(0, "end")

        # ==========================================
        # COMANDOS CUSTOM
        # ==========================================


        if comando == "/za_warudo":

            self.escrever(
                "🕒 TOKI WO TOMARE!\n"
            )

            self.win.configure(bg="#222")

            return

        elif comando == "/clear":

            self.output.delete(
                "1.0",
                "end"
            )

            return

        elif comando == "/help":

            self.escrever(
                """
COMANDOS:

/help
/reparar
/clear
/za_warudo

Você também pode usar comandos reais do Windows.
"""
            )

            return

        # ==========================================
        # COMANDOS WINDOWS
        # ==========================================

        try:

            resultado = subprocess.check_output(
                comando,
                shell=True,
                stderr=subprocess.STDOUT,
                text=True
            )

            self.escrever(resultado)

        except Exception as e:

            self.escrever(
                f"\nERRO:\n{e}\n"
            )