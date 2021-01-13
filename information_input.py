from GUI import SpinBox, ScrollBox, Button, StaticImage
from constants import BUTTONS_PASS, BUTTONS_ACTIVE, FONTS, IMAGES, BUTTONS
from save import save_new_player, restart_game
import pygame


def information_input(all_sprites, button_group, screen, cursor):
    spinbox = SpinBox(810, 700, 290, 150)
    buttons = [Button(0, 0, 400, 100, images[0], images[1], images[1], [all_sprites, button_group], cursor, None)
               for i, images in enumerate(zip(BUTTONS_PASS, BUTTONS_ACTIVE))]
    scroll1 = ScrollBox(70, 65, 400, 700, 70, 800, buttons, 5, 150)
    buttons = [Button(0, 0, 400, 100, images[0], images[1], images[1], [all_sprites, button_group], cursor, None)
               for i, images in enumerate(zip(BUTTONS_PASS, BUTTONS_ACTIVE))]
    continue_btn = Button(660, 860, 600, 150, BUTTONS["continue1"], BUTTONS["continue2"], BUTTONS["continue2"],
                          [all_sprites, button_group], cursor, None)
    scroll2 = ScrollBox(1450, 65, 400, 700, 1450, 800, buttons, 5, 150)
    StaticImage([all_sprites], IMAGES['woman'], 873, 188)
    StaticImage([all_sprites], IMAGES['field'], 810, 700)

    while True:
        screen.fill(pygame.Color("#DF1479"))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                all_sprites.empty()
                button_group.empty()
                return 'menu'

            if continue_btn.is_mouse_button_up(event):
                if spinbox.get_value() and scroll1.get_collection() and scroll2.get_collection():
                    all_sprites.empty()
                    button_group.empty()
                    player_data = {'age': spinbox.get_value(),
                                   'characters': ' '.join(scroll1.get_collection()),
                                   'characters_partner': ' '.join(scroll2.get_collection())}
                    restart_game()
                    save_new_player(player_data)
                    return 'continue'

            for name in 'scroll1', 'scroll2', 'spinbox', 'button_group':
                locals()[name].update(event)

        all_sprites.draw(screen)
        for name in 'scroll1', 'scroll2':
            locals()[name].render(screen, 'black', FONTS['Standard-35'], 32, 30)
        spinbox.render(screen, 'black', FONTS['RammettoOne-Regular-90'])
        cursor.update()

        pygame.display.flip()
