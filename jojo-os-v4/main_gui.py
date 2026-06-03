# main_gui.py
import tkinter as tk
import os 
import subprocess 
import sys
import dotenv


# froms
from dotenv import load_dotenv
from pygame import mixer
from core.ia_system import responder, garantir_user
from core.system.terminal_window import TerminalWindow
from core.file_manager import FileManager
from core.battle_system import criar_lutador, turno_batalha
from core.file_manager import FileManager
# import-Module venv

import json

load_dotenv()

# from core.login_in_window import LoginSystem
from core.debugger_window import JoJoDebugger
from core.login_in_window import LoginWindow

# IMPORT DO TEMA JOJO E HACKER
from ui.themes.jojo_theme import JoJoTheme
from ui.theme_manager import Theme
from core.ia_window import abrir_janela_ia
from core.calc_window import JoJoCalc
from ui.menacing_animation import start_menacing
from ui.themes.hacker_theme import HackerTheme
from ui.widgets.draggable_icon import DraggableIcon
from ui.widgets.grid_system import snap_to_grid

def enviar_mensagem(self):
    texto = self.input.get()

    # pega usuário logado
    user = self.current_user  

    resposta = responder(user, texto)

    self.chat_box.insert("end", f"\nVocê: {texto}")
    self.chat_box.insert("end", f"\nIA: {resposta}")

    self.input.delete(0, "end")
# CARREGAR VARIÁVEIS
from core.security import carregar_db_seguro
def reparar_sistema():
    print("🔧 Tentando reparar sistema...")

    # 📁 Garante pasta data
    if not os.path.exists("data"):
        os.makedirs("data")
        print("📁 Pasta 'data' criada")

    # 🔑 Corrige system_key.json
    key_path = "data/system_key.json"
    if not os.path.exists(key_path):
        with open(key_path, "w") as f:
            json.dump({"key": "default_key_123"}, f, indent=4)
        print("🔑 system_key.json criado")

    else:
        try:
            with open(key_path) as f:
                data = json.load(f)

            if "key" not in data:
                raise Exception("key inválida")

        except:
            with open(key_path, "w") as f:
                json.dump({"key": "default_key_123"}, f, indent=4)
            print("🔄 system_key.json corrigido")

    # 👥 Corrige users.json se estiver quebrado
    users_path = "data/users.json"
    if os.path.exists(users_path):
        try:
            with open(users_path) as f:
                json.load(f)
        except:
            print("⚠️ users.json corrompido → resetando")
            with open(users_path, "w") as f:
                json.dump({"data": {}, "assinatura": ""}, f, indent=4)

    print("✅ Reparação concluída")
    
class JoJoOS:
    mixer.init()
    def __init__(self, root):
        self.root = root
        
        # Definições iniciais de tema
        self.skin_mode = "JOJO"
        self.current_theme = JoJoTheme
        
        self.root.title("JOJO-OS v4.0 // BIZARRE ADVENTURE")
        self.root.geometry("1000x700")
        self.root.configure(bg=self.current_theme.BLACK)

        # Barra Superior Estilizada
        self.top_bar = tk.Frame(root, bg=self.current_theme.PURPLE, height=40)
        self.top_bar.pack(side="top", fill="x")
        
        self.title_label = tk.Label(self.top_bar, text="⭐ JOJO-OS: GOLDEN EXPERIENCE EDITION", 
                 fg=self.current_theme.GOLD, bg=self.current_theme.PURPLE, 
                 font=("Impact", 14, "bold"))
        self.title_label.pack(side="left", padx=20)

        # Área de Trabalho
        self.canvas = tk.Canvas(root, bg=self.current_theme.BLACK, highlightthickness=0)
        self.canvas.pack(expand=True, fill="both")
        
        self.btn_skin = tk.Button(self.top_bar, text="🔄 ALTERAR SKIN", 
                                command=self.toggle_skin,
                                bg=self.current_theme.PURPLE, fg=self.current_theme.GOLD,
                                font=("Impact", 10))
        self.btn_skin.pack(side="right", padx=10)

        # Lista para armazenar ícones e recriar ao mudar a skin
        self.icons_list = []
        self.icon_positions = self.load_icon_positions()
        self.command_window = None
        # Variáveis de estado do usuário
        self.current_user = None
        self.is_admin = False
        self.stand_theme = None # Cores do stand escolhido para personalizar a interface

    def load_icon_positions(self):
        path = "data/icon_positions.json"

        try:
            os.makedirs("data", exist_ok=True)
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as arquivo:
                    dados = json.load(arquivo)
                    if isinstance(dados, dict):
                        return dados
        except Exception:
            pass

        return {}

    def save_icon_positions(self):
        path = "data/icon_positions.json"

        try:
            # Cria a pasta 'data' se ela não existir
            os.makedirs("data", exist_ok=True)

            # O 'w' já cria o arquivo automaticamente se ele não existir
            with open(path, "w", encoding="utf-8") as arquivo:
                json.dump(self.icon_positions, arquivo, indent=4)

        except Exception as e:
            print(f"Erro ao salvar o arquivo: {e}")

    def grid_system(self, x, y):
        return snap_to_grid(x, y)

    def draggle_icon(self, widget):
        DraggableIcon(self.canvas, widget)

    def run_browser(self):
        from ui.browser import BrowserApp
        browser_win = tk.Toplevel(self.root)
        BrowserApp(browser_win)
    def open_battle(self):

        from battle.battle_in_window import BattleWindow
        from core.battle_system import criar_lutador

        if not self.current_user:
            print("⚠️ Nenhum usuário logado")
            return

        escolha_win = tk.Toplevel(self.root)

        escolha_win.title("⚔️ ESCOLHA SEU STAND")
        escolha_win.geometry("850x650")
        escolha_win.configure(bg="black")

        tk.Label(
            escolha_win,
            text="⚔️ ESCOLHA SEU STAND ⚔️",
            fg="gold",
            bg="black",
            font=("Impact", 28)
        ).pack(pady=20)

        STANDS = {

            "Star Platinum": {
                "cor": "#5E60CE",
                "desc": "Velocidade absurda e ORA ORA ORA!",
                "power": 10,
                "speed": 10,
                "range": 4,
                "skill": "ORA ORA BARRAGE"
            },

            "The World": {
                "cor": "#FFD60A",
                "desc": "ZA WARUDO! O tempo para.",
                "power": 10,
                "speed": 9,
                "range": 5,
                "skill": "TIME STOP"
            },

            "Killer Queen": {
                "cor": "#FF4D6D",
                "desc": "Explosões silenciosas.",
                "power": 8,
                "speed": 7,
                "range": 6,
                "skill": "BITE THE DUST"
            },

            "D4C": {
                "cor": "#80ED99",
                "desc": "Dimensões infinitas.",
                "power": 9,
                "speed": 7,
                "range": 8,
                "skill": "LOVE TRAIN"
            },

            "Wonder of U": {
                "cor": "#9D4EDD",
                "desc": "Calamidade inevitável.",
                "power": 8,
                "speed": 6,
                "range": 10,
                "skill": "CALAMITY"
            }
        }

        container = tk.Frame(
            escolha_win,
            bg="black"
        )

        container.pack(
            expand=True,
            fill="both"
        )
        def open_files(self):

            FileManager(self.root)
        def selecionar(stand):

            escolha_win.destroy()

            self.jogador_atual = criar_lutador(stand)

            BattleWindow(
                self.root,
                self.current_user,
                stand
            )

        for stand, info in STANDS.items():

            card = tk.Frame(
                container,
                bg="#111",
                highlightbackground=info["cor"],
                highlightthickness=3,
                bd=0
            )

            card.pack(
                pady=10,
                padx=20,
                fill="x"
            )

            tk.Label(
                card,
                text=stand,
                fg=info["cor"],
                bg="#111",
                font=("Impact", 24)
            ).pack(pady=(10, 0))

            tk.Label(
                card,
                text=info["desc"],
                fg="white",
                bg="#111",
                font=("Courier New", 10)
            ).pack()

            stats = (
                f"⚔️ POWER: {info['power']}    "
                f"⚡ SPEED: {info['speed']}    "
                f"🎯 RANGE: {info['range']}"
            )

            tk.Label(
                card,
                text=stats,
                fg="gold",
                bg="#111",
                font=("Impact", 12)
            ).pack(pady=5)

            tk.Label(
                card,
                text=f"🔥 SPECIAL: {info['skill']}",
                fg="#ffcc00",
                bg="#111",
                font=("Impact", 14)
            ).pack()

            tk.Button(
                card,
                text="⚔️ ESCOLHER",
                bg=info["cor"],
                fg="black",
                font=("Impact", 14),
                bd=0,
                width=20,
                cursor="hand2",
                command=lambda s=stand: selecionar(s)
            ).pack(pady=10)
    def open_files(self):

        FileManager(self.root)
    def open_terminal(self):

        TerminalWindow(self.root)
    def render_icons(self):
        """Desenha os ícones dependendo da skin ativa"""
        for icon in self.icons_list:
            icon.destroy()
        self.icons_list.clear()

        if self.skin_mode == "JOJO":
            self.add_icon(
    "Terminal",
    "💻",
    self.open_terminal,
    750,
    220,
    "HERMIT PURPLE"
)
            self.add_icon("Calculadora", "🔢", self.open_calc, 50, 50, "STAR PLATINUM", "calc")
            self.add_icon("Heaven's Door IA", "📖", self.open_ia, 150, 50, "ROHAN KISHIBE", "ia")
            self.add_icon("Menacing", "ゴ", self.open_menacing, 250, 50, "DIO BRANDO", "menacing")
            self.add_icon("Battle", "⚔️", self.open_battle, 350, 50, "STAND FIGHT", "battle")
            self.add_icon("Killer Queen", "💣", self.open_antivirus, 50, 200, "YOSHIKAGE KIRA", "antivirus")
            self.add_icon("Games", "🕹️", self.run_pygame, 250, 200, "D'ARBY THE PLAYER", "games")
            self.add_icon("Internet", "🌐", self.run_browser, 400, 200, "D'ARBY THE PLAYER", "explorer")
            self.add_icon("Debugger", "🔍", self.open_debugger, 500, 200, "HIEROPHANT GREEN", "debugger")
            self.add_icon("Terminal", "💻", self.open_terminal, 750, 200, "HERMIT PURPLE")
            self.add_icon("Sticky Fingers", "📂", self.open_files, 750, 50, "BRUNO BUCCIARATI" )
        else:
            self.add_icon("Calc.exe", "📟", self.open_calc, 50, 50, "DECRYPTOR", "calc")
            self.add_icon("Neural_Net", "💾", self.open_ia, 250, 50, "DATABASE", "ia")
            self.add_icon("Glitcher", "⚡", self.open_menacing, 250, 50, "OVERRIDE", "menacing")
            self.add_icon("Firewall", "🧨", self.open_antivirus, 50, 200, "BOMB_SCAN", "antivirus")
            self.add_icon("Emulators", "🎮", self.run_pygame, 250, 200, "PLAYER_SESS", "games")
            self.add_icon("Browser", "🌐", self.run_browser, 400, 200, "D'ARBY THE PLAYER", "browser")
            self.add_icon("Debugger", "🔍", self.open_debugger, 500, 200, "HIEROPHANT GREEN", "debugger")
            self.add_icon("Battle", "⚔️", self.open_battle, 600, 50, "STAND FIGHT", "battle")
            self.add_icon("Comandos", "💻", self.open_command_window, 650, 200, "SHELL", "commands")

    def toggle_skin(self):
        if self.skin_mode == "JOJO":
            self.skin_mode = "HACKER"
            self.current_theme = HackerTheme
            self.title_label.configure(text="💻 CLEITAN-OS: MODO TERMINAL ATIVADO", font=("Courier New", 14, "bold"))
            self.root.title("CLEITAN-OS v4.0 // HACKER EDITION")
        else:
            self.skin_mode = "JOJO"
            self.current_theme = JoJoTheme
            self.title_label.configure(text="⭐ JOJO-OS: GOLDEN EXPERIENCE EDITION", font=("Impact", 14, "bold"))
            self.root.title("JOJO-OS v4.0 // BIZARRE ADVENTURE")

        self.root.configure(bg=self.current_theme.BLACK)
        self.top_bar.configure(bg=self.current_theme.PURPLE)
        self.canvas.configure(bg=self.current_theme.BLACK)
        self.btn_skin.configure(bg=self.current_theme.PURPLE, fg=self.current_theme.GOLD)
        self.title_label.configure(fg=self.current_theme.GOLD, bg=self.current_theme.PURPLE)
        
        self.render_icons()

    def add_icon(self, name, symbol, command, x, y, stand_name, icon_key=None):
        icon_key = icon_key or name.lower()
        pos_x, pos_y = self.icon_positions.get(icon_key, self.grid_system(x, y))

        icon_frame = tk.Frame(self.canvas, bg=self.current_theme.BLACK)
        icon_frame.place(x=pos_x, y=pos_y)
        self.icons_list.append(icon_frame)

        font_main = "Impact" if self.skin_mode == "JOJO" else "Courier New"
        font_sub = ("Courier New", 8, "bold") if self.skin_mode == "JOJO" else ("Consolas", 8, "bold")
        relief_btn = "raised" if self.skin_mode == "JOJO" else "flat"

        btn = tk.Button(icon_frame, text=f"{symbol}", command=command,
                        bg=self.current_theme.PURPLE, fg=self.current_theme.GOLD, font=(font_main, 30),
                        bd=4, relief=relief_btn, activebackground=self.current_theme.PINK,
                        activeforeground=self.current_theme.WHITE, width=3, height=1)
        btn.pack()

        tk.Label(icon_frame, text=name, fg=self.current_theme.WHITE, bg=self.current_theme.BLACK,
                font=(font_main, 10)).pack()
        tk.Label(icon_frame, text=f"[{stand_name}]", fg=self.current_theme.PINK, bg=self.current_theme.BLACK,
                font=font_sub).pack()

        DraggableIcon(self.canvas, icon_frame)

        def atualizar_posicao(event=None):
            self.icon_positions[icon_key] = [icon_frame.winfo_x(), icon_frame.winfo_y()]
            self.save_icon_positions()

        icon_frame.bind("<ButtonRelease-1>", atualizar_posicao)

    def open_command_window(self):
        from core.command_window import CommandWindow

        if self.command_window and self.command_window.winfo_exists():
            self.command_window.focus_force()
            return

        self.command_window = CommandWindow(self.root, self)

    def open_debugger(self):
        JoJoDebugger(self.root, self.current_theme)

    def open_ia(self):
        # Enviar o objeto da aplicação para a IA, para que ela possa executar comandos
        abrir_janela_ia(self)

    def open_menacing(self):
        start_menacing()
    def handle_security_breach(self, db):
        import tkinter as tk
        from tkinter import messagebox
        import os

        win = tk.Toplevel(self.root)
        win.title("⚠️ SISTEMA COMPROMETIDO")
        win.geometry("400x200")
        win.configure(bg="black")

        tk.Label(win, text="POSSÍVEL HACK DETECTADO!",
                fg="red", bg="black", font=("Impact", 14)).pack(pady=10)

        tk.Label(win, text="Digite a senha MASTER:",
                fg="white", bg="black").pack()

        entry = tk.Entry(win, show="*")
        entry.pack(pady=10)

        

        def verificar():
            master = os.getenv("MASTER_PASSWORD")

            if entry.get() == master:
                from core.security import salvar_db_seguro

                salvar_db_seguro(db, "data/users.json")

                messagebox.showinfo("SUCESSO", "Banco restaurado!")
                win.destroy()
            else:
                messagebox.showerror("ERRO", "Senha incorreta!")

        tk.Button(win, text="RESTAURAR",
                command=verificar,
                bg="purple", fg="gold").pack(pady=10)
    def run_pygame(self):
        try:
            self.erro_lbl = tk.Label(self.root, text="", bg="black")
            self.erro_lbl.pack()
            # Roda o jogo como um processo separado usando o mesmo interpretador
            base_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.abspath(os.path.join(base_dir, ".."))
            script_path = os.path.join("jojo-os-v4", "ui", "games", "main.py")
            if not os.path.exists(script_path):
                raise FileNotFoundError(f"Arquivo do jogo não encontrado: {script_path}")
            # Mensagens identificadas para o terminal do usuário antes de iniciar
            prefix = "[JOJO-OS]"
            interpreter = sys.executable
            cwd = os.path.dirname(script_path)
            try:
                print(f"{prefix} Interpreter: {interpreter}")
                print(f"{prefix} Script: {script_path}")
                print(f"{prefix} Working dir: {cwd}")
                sys.stdout.flush()
            except Exception:
                pass

            # Monta o comando que será mostrado e executado no terminal do usuário
            cmdline = f'cd /d "{cwd}" && "{interpreter}" "{script_path}"'
            try:
                print(f"{prefix} Command: {cmdline}")
                sys.stdout.flush()
            except Exception:
                pass

            # Abra uma nova janela do cmd e execute o comando (Windows)
            try:
                subprocess.Popen(["cmd", "/c", "start", "cmd", "/k", cmdline], cwd=cwd)
            except Exception:
                # fallback: executar diretamente caso não consiga abrir nova janela
                subprocess.Popen([interpreter, script_path], cwd=cwd)
        except Exception as e:
            self.show_error_no_sound("OH NO!", f"HORY SHET! Não foi possível iniciar o jogo: {e}")

    def open_antivirus(self):
        self.antivirus_window()

    def show_error_no_sound(self, title, message):
        win = tk.Toplevel(self.root)
        win.title(title)
        win.geometry("420x140")
        win.configure(bg=self.current_theme.BLACK)
        win.transient(self.root)
        win.resizable(False, False)

        tk.Label(win, text=title, fg=self.current_theme.PINK, bg=self.current_theme.BLACK, font=("Impact", 14, "bold")).pack(pady=(10, 5))
        tk.Label(win, text=message, fg=self.current_theme.GOLD, bg=self.current_theme.BLACK, font=("Courier New", 10), wraplength=380, justify="center").pack(padx=10)

        btn_frame = tk.Frame(win, bg=self.current_theme.BLACK)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="OK", width=10, bg=self.current_theme.PURPLE, fg=self.current_theme.GOLD,
                  command=win.destroy).pack()

        # Evita que outros widgets da janela principal recebam foco até fechar
        win.grab_set()

    def clear_and_play(self, log):
        try:
            # limpa o log
            log.delete("1.0", tk.END)
            # caminho do arquivo de som na pasta 'soms' na raiz do projeto
            base_dir = os.path.dirname(os.path.abspath(__file__))
            # como este arquivo está dentro de jojo-os-v4, sobe um nível para encontrar 'soms'
            project_root = os.path.abspath(os.path.join(base_dir, ".."))
            sound_path = os.path.join(project_root, "soms", "bites-dust.wav")
            if not os.path.exists(sound_path):
                raise FileNotFoundError(f"Arquivo de som não encontrado: {sound_path}")
            mixer.Sound(sound_path).play()
        except Exception as e:
            self.show_error_no_sound("OH NO!", f"Não foi possível tocar som: {e}")

    def antivirus_window(self):
        project_root = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
        win = tk.Toplevel(self.root)
        titulo_win = "KILLER QUEEN // BOMB SCANNER" if self.skin_mode == "JOJO" else "CLEITAN-OS // ROOT SCANNER"
        win.title(titulo_win)
        win.geometry("500x400")
        win.configure(bg=self.current_theme.BLACK)
        if self.skin_mode == "JOJO":
            try:
                sound_path = os.path.join(project_root, "soms", "killer-spawn.ogg")
            except Exception as e:
                self.show_error_no_sound("OH NO!", f"Não foi possível tocar som: {e}")
            titulo_label = "💣 KILLER QUEEN JA TOCOU NOS ARQUIVOS" if self.skin_mode == "JOJO" else "💾 VARRENDO DIRETÓRIOS DO SISTEMA..."
            tk.Label(win, text=titulo_label, 
                    fg=self.current_theme.PINK, bg=self.current_theme.BLACK, font=("Impact", 14)).pack(pady=20)
            
            log = tk.Text(win, bg="#1A1A1A", fg=self.current_theme.GOLD, height=12, font=("Courier New", 10))
            log.pack(padx=20, pady=10, fill="both", expand=True)
            
            msg_scan = "[*] Procurando por Stands inimigos...\n" if self.skin_mode == "JOJO" else "[*] Analisando pacotes de rede e vulnerabilidades...\n"
            msg_end = "[*] NENHUM STAND ENCONTRADO!\n" if self.skin_mode == "JOJO" else "[*] STATUS: SISTEMA SEGURO!\n"
            
            log.insert("1.0", msg_scan)
            log.insert(tk.END, msg_end)
            
            btn_text = "MADE IN HEAVEN (LIMPAR)" if self.skin_mode == "JOJO" else "PURGE_LOGS (LIMPAR)"
            tk.Button(win, text=btn_text, bg=self.current_theme.PURPLE, fg=self.current_theme.GOLD,
            font=("Impact", 12), command=lambda: self.clear_and_play(log)).pack(pady=10)
        else:
            sound_path = os.path.join(project_root, "soms", "inutil.wav")

            tk.Label(win, text="💾 VARRENDO DIRETÓRIOS DO SISTEMA...", 
                    fg=self.current_theme.PINK, bg=self.current_theme.BLACK, font=("Impact", 14)).pack(pady=20)
            
            log = tk.Text(win, bg="#1A1A1A", fg=self.current_theme.GOLD, height=12, font=("Courier New", 10))
            log.pack(padx=20, pady=10, fill="both", expand=True)
            
            msg_scan = "[*] Analisando pacotes de rede e vulnerabilidades...\n"
            msg_end = "[*] STATUS: SISTEMA SEGURO!\n"
            
            log.insert("1.0", msg_scan)
            log.insert(tk.END, msg_end)
            
            tk.Button(win, text="PURGE_LOGS (LIMPAR)", bg=self.current_theme.PURPLE, fg=self.current_theme.GOLD,
            font=("Impact", 12), command=lambda: self.clear_and_play(log)).pack(pady=10)

    def open_admin_panel(self):
        win = tk.Toplevel(self.root)
        win.title("ADMIN CONTROL PANEL")
        win.geometry("300x200")
        win.configure(bg="black")
        tk.Label(win, text="GERENCIAMENTO DE STANDS", fg="gold", bg="black").pack(pady=20)
        tk.Button(win, text="Resetar system_state.json", command=lambda: os.remove("system_state.json")).pack()

    def logout(self):
        # Esconde tudo e volta para o login
        self.root.withdraw()
        # Remove o botão de logout antigo para não duplicar quando voltar
        
        if hasattr(self, "btn_logout"):

            self.btn_logout.destroy()
        self.chamar_login()

    def open_piano(self):
        from ui.piano.main import PianoWindow
        PianoWindow(self.root, self.current_theme)
    def chamar_login(self):
        """Prepara o ambiente e chama a autenticação"""
        # Força o processamento de eventos antes de esconder para evitar erro de desenho
        self.root.update()
        self.root.withdraw()
        
        # Chama a classe que criamos acima
        LoginWindow(self.root, self.current_theme, self.liberar_sistema)

    def liberar_sistema(self, user, is_admin=False, theme_data=None):
        self.current_user = user
        self.is_admin = is_admin
        self.stand_theme = theme_data # Cores vindas do stand escolhido

        # Atualiza o tema atual com as cores do Stand de Admin
        # Isso evita que o render_icons procure cores que não existem
        self.current_theme.BLACK = self.stand_theme["bg"]
        self.current_theme.PURPLE = self.stand_theme["accent"]
        self.current_theme.GOLD = self.stand_theme["fg"]
        
        # Aplicar cores na interface principal
        self.root.configure(bg=self.current_theme.BLACK)
        self.top_bar.configure(bg=self.current_theme.PURPLE)
        self.canvas.configure(bg=self.current_theme.BLACK)
        
        self.root.deiconify() # Mostra a janela principal
        
        # --- SEGREDO: THE WORLD / ZA WARUDO ---
        if user in ["the world", "za warudo"]:
            self.trigger_time_stop()
        
        # AGORA SIM desenhamos os ícones com as cores certas
        self.render_icons()

    def trigger_time_stop(self):
        # # """Efeito visual de congelamento de tempo"""
        original_bg = self.canvas.cget("bg")
        # Inverte as cores para tons de cinza rapidamente
        self.canvas.configure(bg="#4D4D4D")
        self.root.update()
        
        # Tocar som de parada do tempo
        self.play_stand_sound("time_stop.wav")
        
        # Após 1 segundo, volta ao normal
        self.root.after(1000, lambda: self.canvas.configure(bg=original_bg))

    def play_stand_sound(self, filename):
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            sound_path = os.path.join(base_dir, "..", "soms", filename)
            mixer.Sound(sound_path).play()
        except:
            pass

    def open_calc(self):
        win = tk.Toplevel(self.root)
        # Se for THE WORLD, manda o comando MUDA, senão manda ORA
        calc_audio = "muda" if "za warudo" in self.current_user.lower() else "ora"
        JoJoCalc(win, theme_atual=self.skin_mode, sound_mode=calc_audio)

if __name__ == "__main__":
    root = tk.Tk()

    print("🔍 Verificando integridade do sistema...")
    processar_eventos = root.update()  # Garante que a janela seja processada antes de continuar
    
    print("funcionando")

    db = carregar_db_seguro("data/users.json")

    app = JoJoOS(root)  # ✅ cria SEMPRE

    # 🚨 Se detectou hack
    if isinstance(db, dict) and db.get("__hack_detected__"):

        print("⚠️ POSSÍVEL INVASÃO DETECTADA!")

        try:
            app.handle_security_breach(db["data"])

        except Exception as e:
            print(f"❌ Erro ao abrir sistema de recuperação: {e}")

            from tkinter import simpledialog, messagebox
            from core.security import salvar_db_seguro

            senha = simpledialog.askstring(
                "RECUPERAÇÃO",
                "Digite a MASTER PASSWORD:",
                show="*"
            )

            master = os.getenv("MASTER_PASSWORD")

            if senha == master:

                salvar_db_seguro(
                    db["data"],
                    "data/users.json"
                )

                messagebox.showinfo(
                    "SUCESSO",
                    "Banco restaurado!"
                )

                db["__hack_detected__"] = False

            else:
                messagebox.showerror(
                    "ERRO",
                    "Senha incorreta!"
                )

                root.destroy()

    else:
        app.chamar_login()

    root.mainloop()