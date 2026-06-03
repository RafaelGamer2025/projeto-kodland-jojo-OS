import tkinter as tk
from tkinter import scrolledtext


class CommandWindow:
    def __init__(self, master, app):
        self.app = app
        self.window = tk.Toplevel(master)
        self.window.title("CLEITAN-OS // COMANDOS")
        self.window.geometry("640x420")
        self.window.configure(bg=app.current_theme.BLACK)
        self.window.transient(master)
        self.window.resizable(False, False)

        self._build_ui()
        self.log("[CLEITAN-OS] Janela de comandos iniciada")
        self.log("Comandos disponíveis: help, clear, open calc, open ia, open browser, open debugger, open battle, open antivirus, open game, open menacing, exit")

    def _build_ui(self):
        title = tk.Label(
            self.window,
            text="💻 CLEITAN-OS // JANELA DE COMANDOS",
            fg=self.app.current_theme.GOLD,
            bg=self.app.current_theme.BLACK,
            font=("Courier New", 14, "bold"),
        )
        title.pack(pady=(12, 6))

        self.output = scrolledtext.ScrolledText(
            self.window,
            bg="#0f0f0f",
            fg=self.app.current_theme.GOLD,
            insertbackground=self.app.current_theme.GOLD,
            font=("Consolas", 10),
            wrap=tk.WORD,
        )
        self.output.pack(fill="both", expand=True, padx=12, pady=(0, 8))

        entry_frame = tk.Frame(self.window, bg=self.app.current_theme.BLACK)
        entry_frame.pack(fill="x", padx=12, pady=(0, 12))

        self.entry = tk.Entry(
            entry_frame,
            bg="#111111",
            fg=self.app.current_theme.WHITE,
            insertbackground=self.app.current_theme.GOLD,
            font=("Consolas", 11),
        )
        self.entry.pack(side="left", fill="x", expand=True)

        tk.Button(
            entry_frame,
            text="EXECUTAR",
            bg=self.app.current_theme.PURPLE,
            fg=self.app.current_theme.GOLD,
            font=("Courier New", 10, "bold"),
            command=self.execute_command,
        ).pack(side="right", padx=(8, 0))

        self.entry.bind("<Return>", lambda _event: self.execute_command())
        self.entry.focus_set()

    def log(self, message):
        self.output.insert(tk.END, f"{message}\n")
        self.output.see(tk.END)

    def execute_command(self):
        command = self.entry.get().strip().lower()
        self.entry.delete(0, tk.END)

        if not command:
            return

        self.log(f"> {command}")

        actions = {
            "help": self._show_help,
            "clear": self._clear_output,
            "open calc": lambda: self.app.open_calc(),
            "open calculator": lambda: self.app.open_calc(),
            "open ia": lambda: self.app.open_ia(),
            "open ai": lambda: self.app.open_ia(),
            "open browser": lambda: self.app.run_browser(),
            "open debugger": lambda: self.app.open_debugger(),
            "open battle": lambda: self.app.open_battle(),
            "open antivirus": lambda: self.app.open_antivirus(),
            "open game": lambda: self.app.run_pygame(),
            "open menacing": lambda: self.app.open_menacing(),
            "exit": self.window.destroy,
            "close": self.window.destroy,
        }

        action = actions.get(command)
        if action is None:
            self.log("Comando inválido. Digite 'help' para ver a lista.")
            return

        action()

    def _show_help(self):
        self.log("help - mostra os comandos")
        self.log("clear - limpa o log")
        self.log("open calc - abre a calculadora")
        self.log("open ia - abre a janela de IA")
        self.log("open browser - abre o navegador")
        self.log("open debugger - abre o debugger")
        self.log("open battle - abre a batalha")
        self.log("open antivirus - abre o antivírus")
        self.log("open game - abre o jogo")
        self.log("open menacing - abre o menacing")
        self.log("exit - fecha esta janela")

    def _clear_output(self):
        self.output.delete("1.0", tk.END)

    def winfo_exists(self):
        return self.window.winfo_exists()

    def focus_force(self):
        self.window.focus_force()
