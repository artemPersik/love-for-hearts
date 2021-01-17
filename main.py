from GUI import Button, Cursor, Slider, VolumeSlider, AllSprites
from information_input import information_input
from main_menu import main_menu
from pause import pause_menu
from constants import IMAGES
from game import main_game
from music import music_sausage, set_volume_all_sounds
from save import get_volume_from_save
import pygame


def main():
    # Инициализация пайгейма
    pygame.init()
    size = WIDTH, HEIGHT = 1920, 1080
    screen = pygame.display.set_mode(size)

    all_sprites = AllSprites()
    man_group = pygame.sprite.Group()
    button_group = pygame.sprite.Group()

    cursor = Cursor(screen, IMAGES['cursor'])
    pygame.mouse.set_visible(False)
    music_sausage()
    set_volume_all_sounds(get_volume_from_save())
    result = 'main menu'
    #result = 'continue'
    clock = pygame.time.Clock()
    FPS = 60

    # Игровой цикл
    while True:
        if result == 'main menu':
            result = main_menu(all_sprites, button_group, screen, cursor, clock, FPS)
        if result == 'continue':
            result = main_game(all_sprites, button_group, man_group, screen, cursor)
        if result == 'new game':
            result = information_input(all_sprites, button_group, screen, cursor)
        if result == 'menu':
            result = pause_menu(all_sprites, button_group, screen, cursor)


if __name__ == '__main__':
    main()
