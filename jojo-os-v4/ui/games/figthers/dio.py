import pygame
import os

from sprites.spritesheet_dio import SpriteSheetDio

# ============================================
# LOAD DIO SHEET
# ============================================

SCRIPT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.dirname(SCRIPT_DIR)

DIO_PATH = os.path.join(
    ROOT_DIR,
    "rio.png"
)

sheet_image = pygame.image.load(
    DIO_PATH
).convert_alpha()

sheet = SpriteSheetDio(sheet_image)

# ============================================
# DIO
# ============================================

class Dio:

    def __init__(self):

        self.x = 400
        self.y = 500

        self.speed = 5

        # direção
        self.direction = 1

        # animação
        self.frame_index = 0
        self.animation_speed = 0.20

        # ====================================
        # WALK FRAMES
        # ====================================

        self.walk_frames = []

        WALK_DATA = [

            (0,   575, 69, 125),
            (69,  575, 69, 125),
            (138, 575, 75, 125),
            (213, 575, 75, 125),
            (288, 575, 75, 125),
            (363, 575, 75, 125),
            (438, 575, 60, 125),
            (498, 575, 60, 125),
            (558, 575, 60, 125)

        ]

        # ====================================
        # CARREGA FRAMES
        # ====================================

        for data in WALK_DATA:

            x, y, w, h = data

            frame = sheet.get_frame(

                x,
                y,
                w,
                h,

                scale=3

            )

            self.walk_frames.append(frame)

        self.image = self.walk_frames[0]

    # ========================================
    # UPDATE
    # ========================================

    def update(self):

        keys = pygame.key.get_pressed()

        moving = False

        # ====================================
        # ESQUERDA
        # ====================================

        if keys[pygame.K_LEFT]:

            self.x -= self.speed

            self.direction = -1

            moving = True

        # ====================================
        # DIREITA
        # ====================================

        if keys[pygame.K_RIGHT]:

            self.x += self.speed

            self.direction = 1

            moving = True

        # ====================================
        # ANIMAÇÃO
        # ====================================

        if moving:

            self.frame_index += self.animation_speed

            if self.frame_index >= len(self.walk_frames):

                self.frame_index = 0

        else:

            self.frame_index = 0

        self.image = self.walk_frames[
            int(self.frame_index)
        ]

    # ========================================
    # DRAW
    # ========================================

    def draw(self, screen):

        image = self.image

        # ====================================
        # FLIP
        # ====================================

        if self.direction == 1:

            image = pygame.transform.flip(
                image,
                True,
                False
            )

        rect = image.get_rect(
            midbottom=(
                self.x,
                self.y
            )
        )

        screen.blit(
            image,
            rect
        )