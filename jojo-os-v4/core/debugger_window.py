# debugger_window.py
import tkinter as tk
from tkinter import ttk, scrolledtext
import subprocess
import os

class JoJoDebugger:
    def __init__(self, parent, theme):
        self.win = tk.Toplevel(parent)
        self.theme = theme
        self.win.title("JOJO-OS // UNIVERSAL DEBUGGER")
        self.win.geometry("700x500")
        self.win.configure(bg=self.theme.BLACK)

        # Estilo TTK
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("TLabel", background=self.theme.BLACK, foreground=self.theme.GOLD)
        self.style.configure("TButton", padding=5)

        self.setup_ui()

    def setup_ui(self):
        # Frame de Entrada
        frame_top = tk.Frame(self.win, bg=self.theme.BLACK)
        frame_top.pack(pady=10, padx=10, fill="x")

        tk.Label(frame_top, text="CAMINHO DO ARQUIVO:", bg=self.theme.BLACK, fg=self.theme.WHITE).pack(side="left")
        self.entry_path = ttk.Entry(frame_top, width=50)
        self.entry_path.pack(side="left", padx=5)

        # Seleção de Linguagem
        self.lang_var = tk.StringVar(value="python")
        langs = ["python", "javascript", "java", "c", "cpp"]
        self.combo_lang = ttk.Combobox(frame_top, textvariable=self.lang_var, values=langs, width=10)
        self.combo_lang.pack(side="left", padx=5)

        # Botão Debug
        self.btn_run = ttk.Button(frame_top, text="RUN DEBUG", command=self.run_process)
        self.btn_run.pack(side="left", padx=5)

        # Área de Output
        self.output_area = scrolledtext.ScrolledText(self.win, bg="#1A1A1A", fg=self.theme.GOLD, font=("Courier New", 10))
        self.output_area.pack(pady=10, padx=10, fill="both", expand=True)

    def run_process(self):
        caminho = self.entry_path.get()
        lang = self.lang_var.get()
        self.output_area.delete("1.0", tk.END)

        if not os.path.exists(caminho):
            self.output_area.insert(tk.END, "[ERRO] Arquivo nao encontrado: {}".format(caminho))
            return

        # Mapeamento de comandos
        comandos = {
            "python": ["python", caminho],
            "javascript": ["node", caminho],
            "java": ["java", caminho],
            "c": ["gcc", caminho, "-o", "temp_out", "&&", "./temp_out"],
            "cpp": ["g++", caminho, "-o", "temp_out", "&&", "./temp_out"]
        }

        try:
            self.output_area.insert(tk.END, "[SISTEMA] Iniciando Debug de {}...\n".format(lang))
            res = subprocess.run(comandos[lang], capture_output=True, text=True, shell=True)
            
            if res.returncode == 0:
                self.output_area.insert(tk.END, "--- SAIDA ---\n{}".format(res.stdout))
            else:
                self.output_area.insert(tk.END, "--- ERRO ENCONTRADO ---\n{}".format(res.stderr))
        except Exception as e:
            self.output_area.insert(tk.END, "Falha critica: {}".format(e))