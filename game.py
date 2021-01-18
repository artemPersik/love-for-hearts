from man import Man, Body, Face, Pants, Hair
from pygame import KEYDOWN, K_ESCAPE
from save import save_game_progress
from pygame.display import flip
from pygame.event import get
from constants import BUTTONS
from player import Player
from music import WIN_SOUND, LOSE_SOUND
from GUI import Button


# Экран основной игры
def main_game(all_sprites, button_group, man_group, screen, cursor):
    player = Player()
    man = Man(Body([man_group, all_sprites]), Face([man_group, all_sprites]),
              Pants([man_group, all_sprites]), Hair([man_group, all_sprites]), player, man_group)

    Button(611, 950, 300, 75, BUTTONS['reject1'], BUTTONS['reject2'], BUTTONS['reject2'],
           [button_group, all_sprites], cursor, man.reject_man)
    Button(1023, 950, 300, 75, BUTTONS['accept1'], BUTTONS['accept2'], BUTTONS['accept2'],
           [button_group, all_sprites], cursor, man.accept_man)

    while True:
        for event in get():

            if event.type == KEYDOWN and event.key == K_ESCAPE:
                save_game_progress(player, man)
                all_sprites.empty()
                button_group.empty()
                man_group.empty()
                return 'menu'
            button_group.update(event)
        if all([i >= 100 for i in player.specifications.values()]):
            all_sprites.empty()
            button_group.empty()
            man_group.empty()
            WIN_SOUND.play()
            return 'win'
        if any([i <= 0 for i in player.specifications.values()]):
            all_sprites.empty()
            button_group.empty()
            man_group.empty()
            LOSE_SOUND.play()
            return 'lose'

        screen.fill('#DF1479')

        man.render(screen)
        player.render(screen)
        all_sprites.draw(screen)

        cursor.update()
        flip()
