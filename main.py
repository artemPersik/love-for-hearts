from system.GUI import Cursor, AllSprites
from scenes.authors import authors_screen
from scenes.win_screen import win_screen
from scenes.lose_screen import lose_screen
from scenes.information_input import information_input
from scenes.main_menu import main_menu
from scenes.pause import pause_menu
from system.constants import IMAGES
from scenes.game import main_game
from system.music import music_sausage, set_volume_all_sounds
from system.save import get_volume_from_save
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

    # Игровой цикл
    while True:
        if result == 'main menu' or result == 'main menu with restart':
            result = main_menu(all_sprites, button_group, screen, cursor, result)
        if result == 'continue':
            result = main_game(all_sprites, button_group, man_group, screen, cursor)
        if result == 'new game' or result == 'restart':
            result = information_input(all_sprites, button_group, screen, cursor, result)
        if result == 'menu':
            result = pause_menu(all_sprites, button_group, screen, cursor)
        if result == 'win':
            result = win_screen(all_sprites, button_group, screen, cursor)
        if result == 'lose':
            result = lose_screen(all_sprites, button_group, screen, cursor)
        if result == 'authors':
            result = authors_screen(all_sprites, button_group, screen, cursor)


if __name__ == '__main__':
    main()
