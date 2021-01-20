from game.man import Man, Body, Face, Pants, Hair
from pygame import KEYDOWN, K_ESCAPE
from system.save import save_game_progress
from pygame.display import flip
from pygame.event import get
from system.constants import BUTTONS, FONTS
from game.player import Player
from system.music import WIN_SOUND, LOSE_SOUND
from system.system import print_text
from system.GUI import Button


# Экран основной игры
def main_game(all_sprites, button_group, man_group, screen, cursor):
    check_point = 50
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
        if all([i >= check_point for i in player.specifications.values()]):
            check_point += 25
            if player.money <= 60:
                player.money += 30
            if player.money >= 120:
                player.money -= 30

        screen.fill('#DF1479')

        man.render(screen)
        player.render(screen)
        all_sprites.draw(screen)
        print_text(screen, 70, 10, 'Ваши характеристики', 'black', FONTS['Pacifico-Regular-60'])
        print_text(screen, 1200, 10, 'Характеристики парнётра', 'black', FONTS['Pacifico-Regular-60'])
        print_text(screen, 70, 800, f'Ваш баланс: {player.money}', 'black', FONTS['Pacifico-Regular-60'])
        print_text(screen, 1098, 1010, '-10 сердец', 'black', FONTS['Pacifico-Regular-30'])
        if man.reject_count < 2:
            print_text(screen, 686, 1010, '+3 сердца', 'black', FONTS['Pacifico-Regular-30'])
        else:
            print_text(screen, 595, 1010, '+3 сердца, -15 к статам', 'black', FONTS['Pacifico-Regular-30'])

        cursor.update()
        flip()
