import pygame
import os
import sys

# Inicializa o Pygame
pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cleitan-OS Game")

# Cores
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Carregar imagens
def load_image(image_name):
    return pygame.image.load(os.path.join('assets', 'imagen', image_name))

# Carregar sons
def load_sound(sound_name):
    return pygame.mixer.Sound(os.path.join('assets', 'sounds', sound_name))

# Função principal do jogo
def main():
    clock = pygame.time.Clock()
    running = True

    # Carregar recursos
    background_image = load_image('background.png')  # Exemplo de imagem
    game_sound = load_sound('game_sound.wav')  # Exemplo de som
    game_sound.play(-1)  # Toca o som em loop

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Atualiza a tela
        screen.fill(BLACK)
        screen.blit(background_image, (0, 0))
        pygame.display.flip()

        # Controla a taxa de quadros
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()