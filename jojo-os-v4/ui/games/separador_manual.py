import os
import shutil
import tkinter as tk

from tkinter import messagebox
from PIL import Image, ImageTk

# =====================================================
# CONFIG
# =====================================================

WINDOW_W = 1400
WINDOW_H = 950

MAX_IMAGE_SIZE = 350

# =====================================================
# CAMINHOS
# =====================================================

SCRIPT_DIR = os.path.dirname(__file__)

ASSETS = os.path.join(
    SCRIPT_DIR,
    "assets"
)

# =====================================================
# VERIFICAR ASSETS
# =====================================================

if not os.path.exists(ASSETS):

    messagebox.showerror(
        "Erro",
        "Pasta assets não encontrada."
    )

    quit()

# =====================================================
# PEGAR PASTAS IGGY
# =====================================================

pastas_iggy = []

for pasta in os.listdir(ASSETS):

    full = os.path.join(
        ASSETS,
        pasta
    )

    if (
        os.path.isdir(full)
        and "iggy" in pasta.lower()
        and pasta.lower() != "iggyventure"
    ):

        pastas_iggy.append(pasta)

# =====================================================
# VERIFICAR
# =====================================================

if not pastas_iggy:

    messagebox.showerror(
        "Erro",
        "Nenhuma pasta _iggy encontrada."
    )

    quit()

# =====================================================
# PEGAR SPRITES
# =====================================================

sprites = []

for pasta in pastas_iggy:

    pasta_path = os.path.join(
        ASSETS,
        pasta
    )

    for file in os.listdir(pasta_path):

        if file.endswith(".png"):

            sprites.append({

                "file": file,

                "folder": pasta,

                "path": os.path.join(
                    pasta_path,
                    file
                )
            })

# =====================================================
# VERIFICAR
# =====================================================

if not sprites:

    messagebox.showerror(
        "Erro",
        "Nenhum sprite encontrado."
    )

    quit()

# =====================================================
# TKINTER
# =====================================================

root = tk.Tk()

root.title("Separador Manual Iggy")

root.geometry(
    f"{WINDOW_W}x{WINDOW_H}"
)

root.configure(bg="#202020")

# =====================================================
# INDEX
# =====================================================

index = 0

# =====================================================
# INFO
# =====================================================

info_label = tk.Label(

    root,

    text="",

    bg="#202020",

    fg="white",

    font=("Arial", 14)
)

info_label.pack(
    pady=10
)

# =====================================================
# PREVIEW FRAME
# =====================================================

preview_frame = tk.Frame(
    root,
    bg="#202020"
)

preview_frame.pack(
    pady=20
)

# =====================================================
# LABELS
# =====================================================

prev_label = tk.Label(
    preview_frame,
    bg="#202020"
)

prev_label.grid(
    row=0,
    column=0,
    padx=20
)

current_label = tk.Label(
    preview_frame,
    bg="#202020"
)

current_label.grid(
    row=0,
    column=1,
    padx=20
)

next_label = tk.Label(
    preview_frame,
    bg="#202020"
)

next_label.grid(
    row=0,
    column=2,
    padx=20
)

# =====================================================
# BOTÕES
# =====================================================

buttons_frame = tk.Frame(
    root,
    bg="#202020"
)

buttons_frame.pack(
    pady=20
)

# =====================================================
# CARREGAR IMAGEM
# =====================================================

def carregar_imagem(path):

    try:

        img = Image.open(path)

        img = img.convert("RGBA")

        w, h = img.size

        scale = min(
            MAX_IMAGE_SIZE / w,
            MAX_IMAGE_SIZE / h
        )

        nw = int(w * scale)
        nh = int(h * scale)

        img = img.resize(
            (nw, nh),
            Image.NEAREST
        )

        return ImageTk.PhotoImage(img)

    except Exception as e:

        print(f"Erro imagem: {e}")

        return None

# =====================================================
# MOSTRAR SPRITE
# =====================================================

def mostrar_sprite():

    global index

    if index >= len(sprites):

        messagebox.showinfo(
            "Fim",
            "Todos sprites analisados."
        )

        root.destroy()

        return

    sprite = sprites[index]

    info_label.config(

        text=(
            f"{index+1}/{len(sprites)}\n\n"
            f"Pasta Atual:\n"
            f"{sprite['folder']}\n\n"
            f"Arquivo:\n"
            f"{sprite['file']}"
        )
    )

    # =================================================
    # ATUAL
    # =================================================

    img = carregar_imagem(
        sprite["path"]
    )

    if img:

        current_label.config(
            image=img
        )

        current_label.image = img

    # =================================================
    # ANTERIOR
    # =================================================

    if index > 0:

        prev = carregar_imagem(
            sprites[index - 1]["path"]
        )

        if prev:

            prev_label.config(
                image=prev
            )

            prev_label.image = prev

    else:

        prev_label.config(image="")

    # =================================================
    # PRÓXIMO
    # =================================================

    if index < len(sprites) - 1:

        nxt = carregar_imagem(
            sprites[index + 1]["path"]
        )

        if nxt:

            next_label.config(
                image=nxt
            )

            next_label.image = nxt

    else:

        next_label.config(image="")

# =====================================================
# MOVER
# =====================================================

def mover(destino):

    global index

    sprite = sprites[index]

    origem = sprite["path"]

    nome = sprite["file"]

    atual = sprite["folder"]

    # =============================================
    # NÃO MOVE
    # =============================================

    if atual == destino:

        index += 1

        mostrar_sprite()

        return

    novo = os.path.join(
        ASSETS,
        destino,
        nome
    )

    # =============================================
    # EXISTE
    # =============================================

    if os.path.exists(novo):

        resp = messagebox.askyesno(

            "Arquivo Existe",

            f"{nome}\n\n"
            "já existe.\n\n"
            "Substituir?"
        )

        if not resp:

            return

        os.remove(novo)

    # =============================================
    # MOVE
    # =============================================

    shutil.move(
        origem,
        novo
    )

    print(
        f"{nome}: {atual} -> {destino}"
    )

    index += 1

    mostrar_sprite()

# =====================================================
# PULAR
# =====================================================

def pular():

    global index

    index += 1

    mostrar_sprite()

# =====================================================
# CRIAR BOTÕES
# =====================================================

for i, pasta in enumerate(pastas_iggy):

    btn = tk.Button(

        buttons_frame,

        text=pasta,

        width=22,

        height=2,

        bg="#404040",

        fg="white",

        font=("Arial", 11),

        command=lambda p=pasta:
            mover(p)
    )

    btn.grid(

        row=i // 3,

        column=i % 3,

        padx=10,

        pady=10
    )

# =====================================================
# BOTÃO PULAR
# =====================================================

skip_btn = tk.Button(

    root,

    text="PULAR (ESC)",

    width=25,

    height=2,

    bg="#803030",

    fg="white",

    font=("Arial", 12),

    command=pular
)

skip_btn.pack(
    pady=20
)

# =====================================================
# ESC
# =====================================================

root.bind(
    "<Escape>",
    lambda e: pular()
)

# =====================================================
# START
# =====================================================

mostrar_sprite()

root.mainloop()