import pygame
import os


# =========t===========================================
# PYGAME
# =====================================================

pygame.init()

WIDTH = 1280
HEIGHT = 720

screen = pygame.display.set_mode(
    (WIDTH, HEIGHT)
)

pygame.display.set_caption(
    "JoJo Engine"
)

clock = pygame.time.Clock()

FPS = 60

# =====================================================
# CORES TRANSPARENTES
# =====================================================

TRANSPARENT_COLORS = [

    (112, 112, 240), # #7070F0
    (56, 56, 104)    # #383868

]

# =====================================================
# SPRITESHEET UNIVERSAL
# =====================================================

class SpriteSheet:

    def __init__(self, image):

        self.sheet = image

    def get_image(

        self,

        frame,
        row,

        width,
        height,

        scale,

        offset_x,
        offset_y
    ):

        # =============================================
        # SUPERFÍCIE
        # =============================================

        image = pygame.Surface(
            (width, height),
            pygame.SRCALPHA
        )

        # =============================================
        # RECORTE
        # =============================================

        image.blit(

            self.sheet,

            (0, 0),

            (

                int((frame * width) + offset_x),

                int((row * height) + offset_y),

                width,
                height
            )
        )

        # =============================================
        # REMOVE FUNDO
        # =============================================

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

        # =============================================
        # ESCALA
        # =============================================

        image = pygame.transform.scale(

            image,

            (
                int(width * scale),
                int(height * scale)
            )
        )

        return image

# =====================================================
# PASTA ASSETS
# =====================================================

SCRIPT_DIR = os.path.dirname(__file__)

ASSETS = os.path.join(
    SCRIPT_DIR,
    "figthers"
)

# =====================================================
# PERSONAGEM
# =====================================================

CURRENT_CHARACTER = "dio_teste"

# =====================================================
# CONFIG DIO
# =====================================================

if CURRENT_CHARACTER == "dio":

    IMAGE_NAME = "rio.png"

    OFFSET_X = 26
    OFFSET_Y = 17

    SCALE = 2

    IDLE = [

        (0, 0, 69, 125),
        (1, 0, 69, 125),
        (2, 0, 69, 125),
        (3, 0, 69, 125)

    ]

    WALK = [

        (0, 4.6, 69, 125),
        (1, 4.6, 69, 125),
        (2, 4.6, 75, 125),
        (3, 4.6, 75, 125),
        (4.1, 4.6, 75, 125),
        (5.06, 4.6, 75, 125),
        (7.59, 4.6, 60, 125),
        (8.55, 4.6, 60, 125),
        (9.5, 4.6, 60, 125)

    ]
# =====================================================
# CONFIG DIO TESTE
# =====================================================

elif CURRENT_CHARACTER == "dio_teste":

    IMAGE_NAME = "rio.png"

    OFFSET_X = 0
    OFFSET_Y = 0

    SCALE = 2

    IDLE = [

        (0, 0, 69, 125),
        (1, 0, 69, 125),
        (2, 0, 69, 125),
        (3, 0, 69, 125)

    ]

    WALK = [

        (0, 4.6, 69, 125),
        (1, 4.6, 69, 125),
        (2, 4.6, 75, 125),
        (3, 4.6, 75, 125),
        (4.1, 4.6, 75, 125),
        (5.06, 4.6, 75, 125),
        (7.59, 4.6, 60, 125),
        (8.55, 4.6, 60, 125),
        (9.5, 4.6, 60, 125)

    ]
# =====================================================
# CONFIG JOTARO
# =====================================================

elif CURRENT_CHARACTER == "jotaro":

    IMAGE_NAME = "jotaro.png"

    OFFSET_X = 0
    OFFSET_Y = 0

    SCALE = 2

    IDLE = [

        (0, 0, 80, 120),
        (1, 0, 80, 120),
        (2, 0, 80, 120),
        (3, 0, 80, 120)

    ]

    WALK = [

        (0, 1, 80, 120),
        (1, 1, 80, 120),
        (2, 1, 80, 120),
        (3, 1, 80, 120)

    ]

# =====================================================
# CONFIG KAKYOIN / IGGY
# =====================================================

elif CURRENT_CHARACTER == "kakyoin":

    IMAGE_NAME = "cachorro.png"

    OFFSET_X = 15
    OFFSET_Y = 17

    SCALE = 3

    IDLE = [

        (0, 0, 169, 139),
        (1, 0, 169, 139),
        (2, 0, 169, 139)

    ]

    WALK = [

        (4, 0, 169, 139),
        (5, 0, 169, 139),
        (6, 0, 169, 139),
        (7, 0, 169, 139)

    ]

# =====================================================
# CARREGAR SPRITESHEET
# =====================================================

SPRITE_PATH = os.path.join(
    ASSETS,
    IMAGE_NAME
)

sheet_image = pygame.image.load(
    SPRITE_PATH
).convert_alpha()

sprite_sheet = SpriteSheet(
    sheet_image
)

# =====================================================
# ANIMAÇÕES
# =====================================================

animations = {

    "idle": [],
    "walk": []

}

# =====================================================
# LOAD IDLE
# =====================================================

for frame_data in IDLE:

    frame = sprite_sheet.get_image(

        frame_data[0],
        frame_data[1],

        frame_data[2],
        frame_data[3],

        SCALE,

        OFFSET_X,
        OFFSET_Y
    )

    animations["idle"].append(
        frame
    )

# =====================================================
# LOAD WALK
# =====================================================

for frame_data in WALK:

    frame = sprite_sheet.get_image(

        frame_data[0],
        frame_data[1],

        frame_data[2],
        frame_data[3],

        SCALE,

        OFFSET_X,
        OFFSET_Y
    )

    animations["walk"].append(
        frame
    )

# =====================================================
# PLAYER
# =====================================================

class Player:

    def __init__(self):

        self.x = WIDTH // 2 + 50
        self.y = 600

        self.speed = 5

        # =============================================
        # SPRITES OLHAM PRA ESQUERDA
        # =============================================

        self.direction = -1

        self.action = "idle"

        self.frame_index = 0

        self.animation_speed = 0.15

        self.image = animations[
            self.action
        ][0]

    # =================================================
    # TROCA AÇÃO
    # =================================================

    def set_action(self, action):

        if self.action != action:

            self.action = action

            self.frame_index = 0

    # =================================================
    # UPDATE
    # =================================================

    def update(self):

        keys = pygame.key.get_pressed()

        moving = False

        # =============================================
        # ESQUERDA
        # =============================================

        if keys[pygame.K_LEFT]:

            self.x -= self.speed

            self.direction = -1

            moving = True

        # =============================================
        # DIREITA
        # =============================================

        if keys[pygame.K_RIGHT]:

            self.x += self.speed

            self.direction = 1

            moving = True

        # =============================================
        # TROCAR AÇÃO
        # =============================================

        if moving:

            self.set_action("walk")

        else:

            self.set_action("idle")

        # =============================================
        # ANIMAÇÃO
        # =============================================

        if moving:

            self.frame_index += self.animation_speed

            if self.frame_index >= len(
                animations[self.action]
            ):

                self.frame_index = 0

        # =============================================
        # FRAME
        # =============================================

        self.image = animations[
            self.action
        ][
            int(self.frame_index)
        ]

        # =============================================
        # FLIP
        # =============================================

        if self.direction == 1:

            self.image = pygame.transform.flip(

                self.image,

                True,
                False
            )

    # =================================================
    # DRAW
    # =================================================

    def draw(self, surface):

        rect = self.image.get_rect(

            midbottom=(

                self.x,
                self.y
            )
        )

        surface.blit(
            self.image,
            rect
        )

# =====================================================
# PLAYER
# =====================================================

player = Player()

# =====================================================
# LOOP
# =====================================================

running = True

while running:

    clock.tick(FPS)

    # =============================================
    # EVENTOS
    # =============================================

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False

    # =============================================
    # UPDATE
    # =============================================

    player.update()

    # =============================================
    # FUNDO
    # =============================================

    screen.fill((20, 20, 20))

    # =============================================
    # CHÃO
    # =============================================

    pygame.draw.rect(

        screen,

        (60, 60, 60),

        (0, 600, WIDTH, 120)
    )

    pygame.draw.line(

        screen,

        (120, 120, 120),

        (0, 620),

        (WIDTH, 620),

        4
    )

    # =============================================
    # PLAYER
    # =============================================

    player.draw(screen)

    # =============================================
    # DEBUG
    # =============================================

    font = pygame.font.SysFont(
        "Arial",
        24
    )

    txt = font.render(

        f"Character: {CURRENT_CHARACTER}",

        True,

        (255,255,255)
    )

    screen.blit(
        txt,
        (20, 20)
    )

    pygame.display.flip()

# =====================================================
# FECHAR
# =====================================================

pygame.quit()