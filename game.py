from man import Man, Body, Face, Pants, Hair
from pygame import KEYDOWN, K_ESCAPE
from save import save_game_progress
from pygame.display import flip
from pygame.event import get
from constants import IMAGES
from player import Player
from GUI import Button


# Экран основной игры
def main_game(all_sprites, button_group, man_group, screen, cursor):
    player = Player()
    man = Man(Body([man_group, all_sprites]), Face([man_group, all_sprites]),
              Pants([man_group, all_sprites]), Hair([man_group, all_sprites]), player, man_group)

    Button(611, 950, 300, 75, IMAGES['reject1'], IMAGES['reject2'], IMAGES['reject2'],
           [button_group, all_sprites], cursor, man.reject_man)
    Button(1023, 950, 300, 75, IMAGES['accept1'], IMAGES['accept2'], IMAGES['accept2'],
           [button_group, all_sprites], cursor, man.accept_man)

    while True:
        for event in get():

            if event.type == KEYDOWN and event.key == K_ESCAPE:
                save_game_progress(player, man)
                all_sprites.empty()
                button_group.empty()
                man_group.empty()
                return
            button_group.update(event)

        screen.fill('#DF1479')

        man.render(screen)
        player.render(screen)
        all_sprites.draw(screen)

        cursor.update()
        flip()
