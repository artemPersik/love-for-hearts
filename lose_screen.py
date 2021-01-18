from pygame.display import flip
from pygame.event import get
import pygame
from constants import BUTTONS, IMAGES
from music import BTN_SOUND
from save import restart_player
from GUI import Button, AnimatedSprite


# Экран основной игры
def lose_screen(all_sprites, button_group, screen, cursor):
    clock = pygame.time.Clock()
    FPS = 120
    continue_button = Button(660, 900, 600, 150, BUTTONS['continue1'], BUTTONS['continue2'], BUTTONS['continue2'],
                             [all_sprites, button_group], cursor, None)
    animation = AnimatedSprite([all_sprites], IMAGES['lose'], 10, 1, 510, 0)

    while True:
        for event in get():
            if continue_button.is_clicked:
                all_sprites.empty()
                button_group.empty()
                restart_player()
                BTN_SOUND.play()
                return 'menu'
            button_group.update(event)

        screen.fill('#DF1479')
        all_sprites.draw(screen)
        animation.update()

        clock.tick(FPS)
        cursor.update()
        flip()
