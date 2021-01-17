from GUI import Button, AnimatedSprite, StaticImage
from constants import IMAGES, BUTTONS
from save import check_null_in_save
from music import BTN_SOUND
import pygame


def main_menu(all_sprites, button_group, screen, cursor, clock, FPS):
    is_new_game = check_null_in_save()
    indent = 250 if is_new_game else 200
    buttons_names = ([] if is_new_game else ['continue_b']) + ['new_game_b', 'options_b', 'authors_b', 'quit_b']
    buttons = {}

    for i, name in enumerate(buttons_names):
        buttons[name] = Button(70, 65 + indent * i, 600, 150,
                               BUTTONS[f'{name[:-2]}1'], BUTTONS[f'{name[:-2]}2'], BUTTONS[f'{name[:-2]}2'],
                               [all_sprites, button_group], cursor, None)

    #AnimatedSprite([all_sprites], IMAGES['heart'], 6, 2, 1100, 53)
    StaticImage([all_sprites], IMAGES["para"], 900, 53)
    buttons['quit_b'].set_func(quit)

    while True:
        for event in pygame.event.get():
            if buttons['new_game_b'].is_clicked:
                all_sprites.empty()
                button_group.empty()
                BTN_SOUND.play()
                return 'new game'

            if 'continue_b' in buttons and buttons['continue_b'].is_clicked:
                all_sprites.empty()
                button_group.empty()
                BTN_SOUND.play()
                return 'continue'

            button_group.update(event)
        screen.fill(pygame.Color("#DF1479"))
        all_sprites.draw(screen)
        cursor.update()
        #clock.tick(FPS)
        pygame.display.flip()