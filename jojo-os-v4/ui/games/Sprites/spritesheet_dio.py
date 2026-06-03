import pygame

# ============================================
# REMOVE CORES DO FUNDO
# ============================================

TRANSPARENT_COLORS = [

    (0, 128, 0),      # GREEN
    (112, 112, 240),  # #7070F0
    (56, 56, 104)     # #383868

]

# ============================================
# DIO SPRITESHEET
# ============================================

class SpriteSheetDio:

    def __init__(self, image):

        self.sheet = image.convert_alpha()

    # ========================================
    # EXTRAIR FRAME
    # ========================================

    def get_frame(

        self,

        x,
        y,

        width,
        height,

        scale=1,
        flip=False
    ):

        # ====================================
        # SURFACE
        # ====================================

        image = pygame.Surface(

            (width, height),

            pygame.SRCALPHA

        ).convert_alpha()

        # ====================================
        # RECORTE
        # ====================================

        image.blit(

            self.sheet,

            (0, 0),

            (x, y, width, height)

        )

        # ====================================
        # REMOVE FUNDO
        # ====================================

        for px in range(width):

            for py in range(height):

                color = image.get_at((px, py))

                rgb = (
                    color.r,
                    color.g,
                    color.b
                )

                if rgb in TRANSPARENT_COLORS:

                    image.set_at(

                        (px, py),

                        (0, 0, 0, 0)

                    )

        # ====================================
        # FLIP
        # ====================================

        if flip:

            image = pygame.transform.flip(

                image,

                True,
                False

            )

        # ====================================
        # SCALE
        # ====================================

        if scale != 1:

            image = pygame.transform.scale(

                image,

                (

                    int(width * scale),
                    int(height * scale)

                )

            )

        return image

