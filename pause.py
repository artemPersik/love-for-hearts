from save import save_settings, get_volume_from_save, restart_game
from GUI import Button, Slider, VolumeSlider
from constants import IMAGES
from system import terminate
from pygame import KEYDOWN, K_ESCAPE
from pygame.display import flip
from pygame.event import get


# Экран паузы во время игры
def pause_menu(all_sprites, button_group, screen, cursor):
    continue_btn = Button(660, 100, 600, 150, IMAGES['continue1'], IMAGES['continue2'], IMAGES['continue2'],
                          [button_group, all_sprites], cursor, None)
    restart_btn = Button(660, 300, 600, 150, IMAGES['restart1'], IMAGES['restart2'], IMAGES['restart2'],
                         [button_group, all_sprites], cursor, None)
    quit_btn = Button(660, 700, 600, 150, IMAGES['quit1'], IMAGES['quit2'], IMAGES['quit2'],
                      [button_group, all_sprites], cursor, terminate)
    volume_slider = VolumeSlider((660, 500), IMAGES['line_slider'], (600, 100), (600, 150),
                                 Slider(IMAGES['slider'], [all_sprites]), [all_sprites], get_volume_from_save())

    while True:
        for event in get():

            if event.type == KEYDOWN and event.key == K_ESCAPE or continue_btn.is_mouse_button_up(event):
                all_sprites.empty()
                button_group.empty()
                save_settings(volume=volume_slider.get_volume())
                return

            if restart_btn.is_mouse_button_up(event):
                all_sprites.empty()
                button_group.empty()
                save_settings(volume=volume_slider.get_volume())
                restart_game()
                return
            button_group.update(event)
            volume_slider.update(event)

        screen.fill('#DF1479')
        all_sprites.draw(screen)

        cursor.update()
        flip()