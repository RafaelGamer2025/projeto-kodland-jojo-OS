# login_in_window.py
import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from core.security import hash_password, salvar_db_seguro, carregar_db_seguro

class LoginWindow:
    def setup_login_ui(self):
        self.limpar_tela()

        tk.Label(self.win, text="LOGIN JOJO-OS", fg=self.theme.GOLD, bg="black",
                font=("Impact", 22)).pack(pady=40)

        tk.Label(self.win, text="USUÁRIO:", fg="white", bg="black").pack()
        self.ent_user = ttk.Entry(self.win)
        self.ent_user.pack(pady=5)

        tk.Label(self.win, text="SENHA:", fg="white", bg="black").pack()
        self.ent_pass = ttk.Entry(self.win, show="*")
        self.ent_pass.pack(pady=5)

        tk.Button(self.win, text="ENTRAR",
                command=self.check_login).pack(pady=20)

        tk.Button(self.win, text="CADASTRAR",
                command=self.tela_cadastro_usuario).pack(pady=10)

        tk.Button(self.win, text="ACESSO REQUIEM",
                command=self.tela_inserir_chave).pack(pady=5)

    def __init__(self, root, theme, on_success):
        self.root = root
        self.win = tk.Toplevel(root)
        self.theme = theme
        self.on_success = on_success
        
        self.db_file = "data/users.json"
        self.secret_file = "data/key_secret.json"
        self.config_file = "data/requiem_init.json"
        
        self.win.title("JOJO-OS // SISTEMA DE ACESSO")
        self.win.geometry("450x600")
        self.win.configure(bg="black")
        self.win.resizable(False, False)
        self.win.grab_set()

        # Lógica principal: Tem conta ou é a primeira vez?
        if not self.verificar_se_existem_usuarios():
            self.tela_pergunta_inicial() # Fluxo de criar conta
        else:
            self.setup_login_ui() # Fluxo de login normal

    def verificar_se_existem_usuarios(self):
        """Verifica se o arquivo de banco de dados existe e não está vazio"""
        if os.path.exists(self.db_file):
            with open(self.db_file, "r") as f:
                try:
                    data = json.load(f)
                    return len(data) > 0
                except:
                    return False
        return False

    def limpar_tela(self):
        for widget in self.win.winfo_children():
            widget.destroy()

    # --- FLUXO DE CADASTRO (PRIMEIRO ACESSO) ---

    def tela_pergunta_inicial(self):
        self.limpar_tela()
        tk.Label(self.win, text="[ SISTEMA VIRGEM ]", fg="red", bg="black", font=("Impact", 20)).pack(pady=30)
        tk.Label(self.win, text="VOCÊ POSSUI A CHAVE REQUIEM?", fg="white", bg="black", font=("Arial", 11)).pack(pady=10)
                
        btn_frame = tk.Frame(self.win, bg="black")
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="SIM, EU TENHO", width=15, bg=self.theme.PURPLE, fg="white", command=self.tela_inserir_chave).pack(side="left", padx=10)
                
        tk.Button(btn_frame, text="NÃO TENHO", width=15, bg="#444", fg="white", command=self.tela_cadastro_usuario).pack(side="left", padx=10)


            # ✅ AGORA SIM A FUNÇÃO EXISTE
    def tela_inserir_chave(self):
        self.limpar_tela()
        tk.Label(self.win, text="PROVE SEU VALOR", fg=self.theme.GOLD, bg="black", font=("Impact", 18)).pack(pady=30)
                
        self.key_ent = ttk.Entry(self.win, show="*")
        self.key_ent.pack(pady=10)
        self.key_ent.focus_set()
                
            
        tk.Button(self.win, text="VERIFICAR", command=self.validar_chave).pack(pady=10)

    def validar_chave(self):
        from core.file_finder import buscar_arquivo

        caminho = buscar_arquivo("key_secret.json")

        if not caminho:
            messagebox.showerror("Erro", "Arquivo key_secret.json não encontrado!")
            return
        with open(caminho, "r") as f:
            chave_real = json.load(f).get("master_key", "")
        if self.key_ent.get() == chave_real:
            self.tela_cadastro_admin()
        else:
            self.erro_lbl.config(text="CHAVE INCORRETA!", fg="red")

    def tela_cadastro_admin(self):
        self.limpar_tela()

        tk.Label(self.win, text="CADASTRAR ADMIN", fg=self.theme.GOLD, bg="black",
                font=("Impact", 15)).pack(pady=20)

        tk.Label(self.win, text="USUÁRIO:", fg="white", bg="black").pack()
        self.reg_user = ttk.Entry(self.win)
        self.reg_user.pack(pady=5)

        tk.Label(self.win, text="SENHA:", fg="white", bg="black").pack()
        self.reg_pass = ttk.Entry(self.win, show="*")
        self.reg_pass.pack(pady=5)

        tk.Label(self.win, text="ESCOLHA SEU STAND (ADMIN):",
                fg="red", bg="black").pack(pady=10)

        # ✅ APENAS ADMIN
        stands_admin = {
            "Tusk ACT 4": {"bg": "#000000", "fg": "#00FFFF", "accent": "#FF0000"},
            "Whitesnake": {"bg": "#000000", "fg": "#FFFFFF", "accent": "#6A0DAD"},
            "Wonder of U": {"bg": "#000000", "fg": "#FFD700", "accent": "#8B0000"},
            "The World": {"bg": "#000000", "fg": "#FFD700", "accent": "#32CD32"},
            "D4C": {"bg": "#000000", "fg": "#FF1493", "accent": "#00008B"}
        }

        for nome, cores in stands_admin.items():
            tk.Button(
                self.win,
                text=nome,
                width=30,
                command=lambda n=nome, c=cores: self.finalizar_cadastro_admin(n, c)
            ).pack(pady=2)
    def garantir_pasta_db(self):
        pasta = os.path.dirname(self.db_file)
        
        if not os.path.exists(pasta):
            os.makedirs(pasta)

    def finalizar_cadastro_admin(self, nome, cores):
        user = self.reg_user.get().strip().lower()
        pw = self.reg_pass.get().strip()

        if not user or not pw:
            messagebox.showerror("Erro", "Preencha tudo!")
            return

        novo_db = {
            user: {
                "password": hash_password(pw),
                "role": "admin",
                "stand": nome,
                "theme_data": cores,
                "historico": []
            }
        }

        self.salvar_usuario(novo_db)
    def salvar_usuario(self, novo_db):
        self.garantir_pasta_db()

        data = {}

        if os.path.exists(self.db_file):
            try:
                with open(self.db_file, "r", encoding="utf-8") as f:
                    data = json.load(f)

                    if not isinstance(data, dict):
                        data = {}

            except Exception as e:
                print("Erro ao ler banco:", e)
                data = {}

        # Junta os dados antigos com os novos
        data.update(novo_db)

        # Salva
        with open(self.db_file, "w", encoding="utf-8") as f:
            salvar_db_seguro(data, self.db_file)
        messagebox.showinfo("Sucesso", "Usuário Admin despertado!")
        self.setup_login_ui()

    # --- FLUXO DE LOGIN (QUANDO JÁ TEM CONTA) ---
    def tela_cadastro_usuario(self):
        self.limpar_tela()

        tk.Label(self.win, text="CRIAR USUÁRIO", fg=self.theme.GOLD, bg="black",
                font=("Impact", 18)).pack(pady=20)

        tk.Label(self.win, text="USUÁRIO:", fg="white", bg="black").pack()
        self.new_user = ttk.Entry(self.win)
        self.new_user.pack(pady=5)

        tk.Label(self.win, text="SENHA:", fg="white", bg="black").pack()
        self.new_pass = ttk.Entry(self.win, show="*")
        self.new_pass.pack(pady=5)

        tk.Label(self.win, text="ESCOLHA SEU STAND:", fg="white", bg="black").pack(pady=10)

        # ✅ APENAS USER
        stands_user = {
            "Star Platinum": {"bg": "#000000", "fg": "#FFD700", "accent": "#8A2BE2"},
            "Killer Queen": {"bg": "#000000", "fg": "#FF69B4", "accent": "#4B0082"},
            "Silver Chariot": {"bg": "#000000", "fg": "#C0C0C0", "accent": "#4682B4"}
        }

        for nome, cores in stands_user.items():
            tk.Button(
                self.win,
                text=nome,
                width=30,
                command=lambda n=nome, c=cores: self.finalizar_cadastro_usuario(n, c)
            ).pack(pady=2)
        self.limpar_tela()

    
    def validar_admin_real(self):
        import json
        import os

        with open("data/key_secret.json") as f:
            master = json.load(f)["master_key"]

        return master == os.getenv("MASTER_KEY")
    def check_login(self):
        try:
            db = carregar_db_seguro(self.db_file)
        except:
            messagebox.showerror("Erro", "Banco corrompido!")
            return

        u = self.ent_user.get().lower().strip()
        p = self.ent_pass.get().strip()

        if u not in db:
            messagebox.showerror("Erro", "Usuário não existe!")
            return

        senha_db = db[u].get("password")

        def senha_valida(salva, digitada):
            try:
                # 1. senha normal
                if salva == digitada:
                    return True

                # 2. senha já em hash
                if salva == hash_password(digitada):
                    return True

                # 3. caso seja dict (seu sistema bugado anterior)
                if isinstance(salva, dict):
                    valor = salva.get("value", "")
                    if valor == digitada:
                        return True
                    if valor == hash_password(digitada):
                        return True

            except:
                pass

            return False

        if senha_valida(senha_db, p):
            # 🔥 AUTO-CORRIGE PRA HASH PADRÃO (SEM QUEBRAR NADA)
            db[u]["password"] = hash_password(p)
            salvar_db_seguro(db, self.db_file)

            self.win.destroy()
            self.on_success(
                u,
                is_admin=db[u]["role"] == "admin" and self.validar_admin_real(),
                theme_data=db[u]["theme_data"]
            )
        else:
            messagebox.showerror("Erro", "Senha incorreta!")
    def login_sucesso(self, u, db):
        self.win.destroy()

        self.on_success(
            u,
            is_admin=db[u]["role"] == "admin" and self.validar_admin_real(),
            theme_data=db[u]["theme_data"]
        )
    def finalizar_cadastro_usuario(self, nome, cores):
        user = self.new_user.get().strip().lower()
        pw = self.new_pass.get().strip()

        if not user or not pw:
            messagebox.showerror("Erro", "Preencha tudo!")
            return

        db = {}
        if os.path.exists(self.db_file):
            with open(self.db_file, "r") as f:
                db = json.load(f)

        if user in db:
            messagebox.showerror("Erro", "Usuário já existe!")
            return

        db[user] = {
            "password": hash_password(pw),
            "role": "user",
            "stand": nome,
            "theme_data": cores,
            "historico": []
        }

        salvar_db_seguro(db, self.db_file)
        messagebox.showinfo("Sucesso", "Usuário criado!")
        self.setup_login_ui()