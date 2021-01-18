from pygame.display import flip
from pygame.event import get
from constants import BUTTONS, IMAGES
from music import BTN_SOUND
from save import restart_player
from GUI import Button, StaticImage


# Экран основной игры
def authors_screen(all_sprites, button_group, screen, cursor):
    continue_button = Button(760, 900, 600, 150, BUTTONS['continue1'], BUTTONS['continue2'], BUTTONS['continue2'],
                             [all_sprites, button_group], cursor, None)
    StaticImage([all_sprites], IMAGES['authors'], 0, 0)

    while True:
        for event in get():
            if continue_button.is_clicked:
                all_sprites.empty()
                button_group.empty()
                restart_player()
                BTN_SOUND.play()
                return 'main menu'
            button_group.update(event)

        screen.fill('#DF1479')
        all_sprites.draw(screen)

        cursor.update()
        flip()
