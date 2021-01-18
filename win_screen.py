from pygame.display import flip
from pygame.event import get
from constants import BUTTONS, IMAGES
from music import BTN_SOUND
from save import restart_player
from GUI import Button, StaticImage


# Экран основной игры
def win_screen(all_sprites, button_group, screen, cursor):
    continue_button = Button(660, 900, 600, 150, BUTTONS['continue1'], BUTTONS['continue2'], BUTTONS['continue2'],
                             [all_sprites, button_group], cursor, None)
    StaticImage([all_sprites], IMAGES['win'], 192, 0, (1536, 864))

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

        cursor.update()
        flip()
