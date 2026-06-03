import pygame
import numpy as np

pygame.mixer.pre_init(
    44100,
    -16,
    2,
    512
)

pygame.init()

pygame.mixer.set_num_channels(128)


class Synth:

    def __init__(self):

        self.cache = {}

    def criar_som(
        self,
        freq,
        duracao=4
    ):

        taxa = 44100

        t = np.linspace(
            0,
            duracao,
            int(taxa * duracao),
            False
        )

        # timbre tipo piano

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
            -t * 1.5
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
            self.cache[freq]
        )