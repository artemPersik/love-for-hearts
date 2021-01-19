from system.save import save_settings, get_volume_from_save, restart_game, restart_player
from system.GUI import Button, Slider, VolumeSlider
from system.constants import BUTTONS, IMAGES, FONTS
from system.system import terminate, print_text
from system.music import BTN_SOUND
from pygame import KEYDOWN, K_ESCAPE
from pygame.display import flip
from pygame.event import get


# Экран паузы во время игры
def pause_menu(all_sprites, button_group, screen, cursor):
    continue_btn = Button(660, 50, 600, 150, BUTTONS['continue1'], BUTTONS['continue2'], BUTTONS['continue2'],
                          [button_group, all_sprites], cursor, None)
    restart_btn = Button(660, 250, 600, 150, BUTTONS['restart1'], BUTTONS['restart2'], BUTTONS['restart2'],
                         [button_group, all_sprites], cursor, None)
    new_game_btn = Button(660, 450, 600, 150, BUTTONS['new_game1'], BUTTONS['new_game2'], BUTTONS['new_game2'],
                         [button_group, all_sprites], cursor, None)
    quit_btn = Button(660, 900, 600, 150, BUTTONS['quit1'], BUTTONS['quit2'], BUTTONS['quit2'],
                      [button_group, all_sprites], cursor, terminate)
    volume_slider = VolumeSlider((660, 700), IMAGES['line_slider'], (600, 100), (600, 150),
                                 Slider(IMAGES['slider'], [all_sprites]), [all_sprites], get_volume_from_save())

    while True:
        for event in get():

            if event.type == KEYDOWN and event.key == K_ESCAPE or continue_btn.is_mouse_button_up(event):
                all_sprites.empty()
                button_group.empty()
                save_settings(volume=volume_slider.get_volume())
                BTN_SOUND.play()
                return 'continue'

            if new_game_btn.is_mouse_button_up(event):
                all_sprites.empty()
                button_group.empty()
                save_settings(volume=volume_slider.get_volume())
                BTN_SOUND.play()
                return 'restart'
            if restart_btn.is_mouse_button_up(event):
                all_sprites.empty()
                button_group.empty()
                save_settings(volume=volume_slider.get_volume())
                restart_player()
                BTN_SOUND.play()
                return 'continue'

            button_group.update(event)
            volume_slider.update(event)

        screen.fill('#DF1479')
        all_sprites.draw(screen)
        print_text(screen, 710, 600, 'Шкала громкости', 'black', FONTS['Pacifico-Regular-60'])

        cursor.update()
        flip()