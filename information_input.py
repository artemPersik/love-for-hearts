from GUI import SpinBox, ScrollBox, Button, StaticImage, Slider
from constants import SCROLL_BUTTONS_ACTIVE, SCROLL_BUTTONS_PASS, FONTS, IMAGES, BUTTONS
from save import save_new_player, restart_game
from music import BTN_SOUND
from system import print_text
import pygame


def information_input(all_sprites, button_group, screen, cursor, result):
    spinbox = SpinBox(810, 700, 290, 150)
    buttons = [Button(0, 0, 400, 100, BUTTONS[passs], BUTTONS[active], BUTTONS[active], [all_sprites, button_group],
                      cursor, None, name=passs[:-1])
               for passs, active in zip(SCROLL_BUTTONS_PASS, SCROLL_BUTTONS_ACTIVE)]
    scroll1 = ScrollBox(120, 130, 400, 700, 70, 900, buttons, 5, 150,
                        Slider(IMAGES['scrollslider'], [all_sprites], pos=(70, 180)))
    buttons = [Button(0, 0, 400, 100, BUTTONS[passs], BUTTONS[active], BUTTONS[active], [all_sprites, button_group],
                      cursor, None, name=passs[:-1])
               for passs, active in zip(SCROLL_BUTTONS_PASS, SCROLL_BUTTONS_ACTIVE)]
    continue_btn = Button(660, 860, 600, 150, BUTTONS["continue1"], BUTTONS["continue2"], BUTTONS["continue2"],
                          [all_sprites, button_group], cursor, None)
    scroll2 = ScrollBox(1400, 130, 400, 700, 1450, 900, buttons, 5, 150,
                        Slider(IMAGES['scrollslider'], [all_sprites], pos=(1850, 180)))
    StaticImage([all_sprites], IMAGES['woman'], 873, 88)
    StaticImage([all_sprites], IMAGES['field'], 810, 700)

    while True:
        screen.fill(pygame.Color("#DF1479"))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                all_sprites.empty()
                button_group.empty()
                return 'main menu' if result == 'new game' else 'menu'

            if continue_btn.is_clicked:
                if spinbox.get_value() and scroll1.get_collection() and scroll2.get_collection():
                    all_sprites.empty()
                    button_group.empty()
                    player_data = {'age': spinbox.get_value(),
                                   'characters': ' '.join(scroll1.get_collection()),
                                   'characters_partner': ' '.join(scroll2.get_collection())}
                    restart_game()
                    save_new_player(player_data)
                    BTN_SOUND.play()
                    return 'continue'

            for name in 'scroll1', 'scroll2', 'spinbox', 'button_group':
                locals()[name].update(event)

        all_sprites.draw(screen)
        print_text(screen, 70, 10, 'Ваши характеристики', 'black', FONTS['Pacifico-Regular-60'])
        print_text(screen, 1200, 10, 'Характеристики партнёра', 'black', FONTS['Pacifico-Regular-60'])
        print_text(screen, 793, 565, 'Ваш возраст', 'black', FONTS['Pacifico-Regular-60'])
        spinbox.render(screen, 'black', FONTS['RammettoOne-Regular-90'])
        cursor.update()

        pygame.display.flip()
