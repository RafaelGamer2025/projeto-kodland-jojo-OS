import tkinter as tk
import pygame
import numpy as np

# ==================================================
# AUDIO
# ==================================================

pygame.mixer.pre_init(
    44100,
    -16,
    2,
    512
)

pygame.init()

pygame.mixer.set_num_channels(128)

# ==================================================
# SYNTH
# ==================================================

class Synth:

    def __init__(self):

        self.cache = {}

    def criar_som(
        self,
        freq,
        duracao=8
    ):

        taxa = 44100

        t = np.linspace(
            0,
            duracao,
            int(taxa * duracao),
            False
        )

        onda = (

            np.sin(
                2 * np.pi * freq * t
            )

            +

            0.5 * np.sin(
                2 * np.pi * freq * 2 * t
            )

            +

            0.25 * np.sin(
                2 * np.pi * freq * 3 * t
            )

        )

        envelope = np.exp(
            -t * 0.3
        )

        onda *= envelope

        onda /= np.max(
            np.abs(onda)
        )

        audio = (
            onda * 32767
        ).astype(np.int16)

        stereo = np.column_stack(
            (audio, audio)
        )

        return pygame.sndarray.make_sound(
            stereo
        )

    def tocar(self, freq):

        if freq not in self.cache:

            self.cache[freq] = (
                self.criar_som(freq)
            )

        canal = pygame.mixer.find_channel(
            True
        )

        canal.play(
            self.cache[freq],
            loops=-1
        )

        return canal

# ==================================================
# PIANO
# ==================================================

synth = Synth()

notas = {

    # OITAVA 2

    "a":130.81,
    "w":138.59,

    "s":146.83,
    "e":155.56,

    "d":164.81,

    "f":174.61,
    "t":185.00,

    "g":196.00,
    "y":207.65,

    "h":220.00,
    "u":233.08,

    "j":246.94,

    # OITAVA 3

    "k":261.63,
    "o":277.18,

    "l":293.66,
    "p":311.13,

    ";":329.63,

    "'":349.23,
    "]":369.99,

    "\\":392.00,

    # OITAVA 4

    "z":415.30,
    "x":466.16,

    "c":493.88,
    "v":523.25,

    "b":554.37,
    "n":587.33,

    "m":622.25,
    ",":659.25,

    ".":698.46,
    "/":783.99,

    # OITAVA 5

    "1":830.61,
    "2":880.00,

    "3":932.33,
    "4":987.77,

    "5":1046.50,
    "6":1108.73,

    "7":1174.66,
    "8":1244.51,

    "9":1318.51,
    "0":1396.91,

    "-":1479.98,
    "=":1567.98
}

teclas_pressionadas = set()

canais_ativos = {}

notas_sustentadas = set()

sustain = False

# ==================================================
# KEY PRESS
# ==================================================

def key_press(event):

    global sustain

    tecla = event.keysym.lower()

    # sustain

    if tecla == "space":

        sustain = not sustain

        if sustain:

            status.config(
                text="SUSTAIN ON"
            )

        else:

            status.config(
                text="SUSTAIN OFF"
            )

            for t in list(
                notas_sustentadas
            ):

                if t in canais_ativos:

                    canais_ativos[t].stop()

                    del canais_ativos[t]

            notas_sustentadas.clear()

        return

    if tecla not in notas:
        return

    if tecla in teclas_pressionadas:
        return

    teclas_pressionadas.add(
        tecla
    )

    canal = synth.tocar(
        notas[tecla]
    )

    canais_ativos[
        tecla
    ] = canal

# ==================================================
# KEY RELEASE
# ==================================================

def key_release(event):

    tecla = event.keysym.lower()

    if tecla not in notas:
        return

    teclas_pressionadas.discard(
        tecla
    )

    if tecla not in canais_ativos:
        return

    if sustain:

        notas_sustentadas.add(
            tecla
        )

        return

    canais_ativos[
        tecla
    ].stop()

    del canais_ativos[
        tecla
    ]

# ==================================================
# JANELA
# ==================================================

root = tk.Tk()

root.title(
    "Piano Python"
)

root.geometry(
    "900x350"
)

root.resizable(
    False,
    False
)

# ==================================================
# CANVAS
# ==================================================

canvas = tk.Canvas(

    root,

    width=880,
    height=250,

    bg="gray"

)

canvas.pack(
    pady=10
)

# ==================================================
# BRANCAS
# ==================================================

brancas = [

    ("C","A"),
    ("D","S"),
    ("E","D"),

    ("F","F"),
    ("G","G"),
    ("A","H"),
    ("B","J")

]

for i,(nota,tecla) in enumerate(
    brancas
):

    x = i * 120

    canvas.create_rectangle(

        x,
        0,

        x+120,
        250,

        fill="white"
    )

    canvas.create_text(

        x+60,
        220,

        text=f"{nota}\n{tecla}",

        font=(
            "Arial",
            12
        )
    )

# ==================================================
# PRETAS
# ==================================================

pretas = [

    ("C#","W",90),
    ("D#","E",210),

    ("F#","T",450),
    ("G#","Y",570),
    ("A#","U",690)

]

for nota,tecla,x in pretas:

    canvas.create_rectangle(

        x,
        0,

        x+60,
        140,

        fill="black"
    )

    canvas.create_text(

        x+30,
        110,

        text=tecla,

        fill="white"
    )

# ==================================================
# STATUS
# ==================================================

status = tk.Label(

    root,

    text="SUSTAIN OFF",

    font=(
        "Arial",
        14
    )

)

status.pack()

# ==================================================
# AJUDA
# ==================================================

info = tk.Label(

    root,

    text=
    "A W S E D F T G Y H U J\nEspaço = Sustain",

    font=(
        "Arial",
        12
    )

)

info.pack()

# ==================================================
# BINDS
# ==================================================

root.bind(
    "<KeyPress>",
    key_press
)

root.bind(
    "<KeyRelease>",
    key_release
)

root.focus_force()

# ==================================================
# LOOP
# ==================================================

root.mainloop()