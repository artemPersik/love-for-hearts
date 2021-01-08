from GUI import Button, Cursor, Slider, VolumeSlider, AllSprites
from save import save_game_progress, restart_game
from constants import IMAGES, CURSOR_IMAGE, FONTS
from man import Man, Body, Face, Pants, Hair
from system import terminate
from pause import pause_menu
from game import main_game
import pygame


def main():
    # Инициализация пайгейма
    pygame.init()
    size = WIDTH, HEIGHT = 1920, 1080
    screen = pygame.display.set_mode(size)

    all_sprites = AllSprites()
    man_group = pygame.sprite.Group()
    button_group = pygame.sprite.Group()

    cursor = Cursor([all_sprites], CURSOR_IMAGE)
    pygame.mouse.set_visible(False)
    clock = pygame.time.Clock()
    FPS = 50

    # Игровой цикл
    while True:
        main_game(all_sprites, button_group, man_group, screen, cursor)
        pause_menu(all_sprites, button_group, screen, cursor)


if __name__ == '__main__':
    main()
