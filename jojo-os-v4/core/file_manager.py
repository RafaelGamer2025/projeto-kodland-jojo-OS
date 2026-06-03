import tkinter as tk
from tkinter import filedialog
import os


class FileManager:

    def __init__(self, master):

        self.win = tk.Toplevel(master)

        self.win.title("📂 STICKY FINGERS FILE SYSTEM")

        self.win.geometry("900x600")

        self.win.configure(bg="black")

        # ===== CAMINHO =====

        self.current_path = os.getcwd()

        # ===== TOPO =====

        top = tk.Frame(
            self.win,
            bg="black"
        )

        top.pack(fill="x")

        self.path_label = tk.Label(
            top,
            text=self.current_path,
            fg="gold",
            bg="black",
            font=("Consolas", 10)
        )

        self.path_label.pack(
            side="left",
            padx=10,
            pady=10
        )

        tk.Button(
            top,
            text="⬆ VOLTAR",
            bg="purple",
            fg="white",
            command=self.voltar
        ).pack(side="right", padx=10)

        # ===== LISTA =====

        self.listbox = tk.Listbox(
            self.win,
            bg="#111",
            fg="lime",
            font=("Consolas", 12)
        )

        self.listbox.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        self.listbox.bind(
            "<Double-Button-1>",
            self.abrir
        )

        # ===== BOTOES =====

        bottom = tk.Frame(
            self.win,
            bg="black"
        )

        bottom.pack(fill="x")

        tk.Button(
            bottom,
            text="🗑 DELETAR",
            bg="red",
            fg="white",
            command=self.deletar
        ).pack(side="left", padx=10, pady=10)

        tk.Button(
            bottom,
            text="📄 NOVO TXT",
            bg="blue",
            fg="white",
            command=self.novo_txt
        ).pack(side="left", padx=10)

        self.atualizar()

    # ======================================================
    # ATUALIZAR
    # ======================================================

    def atualizar(self):

        self.listbox.delete(0, "end")

        self.path_label.config(
            text=self.current_path
        )

        try:

            arquivos = os.listdir(
                self.current_path
            )

            for arq in arquivos:

                full = os.path.join(
                    self.current_path,
                    arq
                )

                if os.path.isdir(full):

                    self.listbox.insert(
                        "end",
                        f"📁 {arq}"
                    )

                else:

                    self.listbox.insert(
                        "end",
                        f"📄 {arq}"
                    )

        except Exception as e:

            print(e)

    # ======================================================
    # ABRIR
    # ======================================================

    def abrir(self, event=None):

        selecionado = self.listbox.get(
            self.listbox.curselection()
        )

        nome = selecionado[2:]

        caminho = os.path.join(
            self.current_path,
            nome
        )

        # ===== PASTA =====

        if os.path.isdir(caminho):

            self.current_path = caminho

            self.atualizar()

        # ===== ARQUIVO =====

        else:

            self.abrir_arquivo(caminho)

    # ======================================================
    # VISUALIZAR ARQUIVO
    # ======================================================

    def abrir_arquivo(self, caminho):

        try:

            with open(
                caminho,
                "r",
                encoding="utf-8"
            ) as f:

                conteudo = f.read()

        except:

            conteudo = "❌ Não foi possível abrir."

        viewer = tk.Toplevel(self.win)

        viewer.title(os.path.basename(caminho))

        viewer.geometry("700x500")

        txt = tk.Text(
            viewer,
            bg="black",
            fg="white",
            insertbackground="white",
            font=("Consolas", 11)
        )

        txt.pack(
            fill="both",
            expand=True
        )

        txt.insert(
            "1.0",
            conteudo
        )

    # ======================================================
    # VOLTAR
    # ======================================================

    def voltar(self):

        novo = os.path.dirname(
            self.current_path
        )

        if novo:

            self.current_path = novo

            self.atualizar()

    # ======================================================
    # DELETAR
    # ======================================================

    def deletar(self):

        try:

            selecionado = self.listbox.get(
                self.listbox.curselection()
            )

            nome = selecionado[2:]

            caminho = os.path.join(
                self.current_path,
                nome
            )

            if os.path.isfile(caminho):

                os.remove(caminho)

            self.atualizar()

        except Exception as e:

            print(e)

    # ======================================================
    # NOVO TXT
    # ======================================================

    def novo_txt(self):

        nome = "novo_arquivo.txt"

        caminho = os.path.join(
            self.current_path,
            nome
        )

        contador = 1

        while os.path.exists(caminho):

            nome = f"novo_arquivo_{contador}.txt"

            caminho = os.path.join(
                self.current_path,
                nome
            )

            contador += 1

        with open(
            caminho,
            "w",
            encoding="utf-8"
        ) as f:

            f.write("JOJO-OS TEXT FILE")

        self.atualizar()