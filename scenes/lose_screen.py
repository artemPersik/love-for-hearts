from pygame.display import flip
from pygame.event import get
import pygame
from system.constants import BUTTONS, IMAGES
from system.music import BTN_SOUND
from system.save import restart_player
from system.GUI import Button, AnimatedSprite


# Экран основной игры
def lose_screen(all_sprites, button_group, screen, cursor):
    clock = pygame.time.Clock()
    FPS = 120
    continue_button = Button(660, 900, 600, 150, BUTTONS['continue1'], BUTTONS['continue2'], BUTTONS['continue2'],
                             [all_sprites, button_group], cursor, None)
    animation = AnimatedSprite([all_sprites], IMAGES['lose'], 10, 1, 510, 0)

    while True:
        for event in get():
            if continue_button.is_mouse_button_up(event):
                all_sprites.empty()
                button_group.empty()
                restart_player()
                BTN_SOUND.play()
                return 'main menu with restart'
            button_group.update(event)

        screen.fill('#DF1479')
        all_sprites.draw(screen)
        animation.update()

        clock.tick(FPS)
        cursor.update()
        flip()
