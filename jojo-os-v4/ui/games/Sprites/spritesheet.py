import pygame

class SpriteSheet():

    def __init__(self, image):

        self.sheet = image

    def get_image(

        self,
        frame,
        row,
        width,
        height,
        scale,
        colour
    ):

        image = pygame.Surface(
            (width, height)
        ).convert_alpha()

        image.blit(

            self.sheet,

            (0, 0),

            (
                (frame * width) + 26,
                (row * height) + 49,

                width,
                height
            )
        )

        image = pygame.transform.scale(

            image,

            (
                int(width * scale),
                int(height * scale)
            )
        )

        image.set_colorkey(colour)

        return image