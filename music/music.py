import pygame
from random import choice

BTS_ALBUM = [f"music/ost/BTS_{i}.wav" for i in range(10)]

# Это функцию можно вызвать в начале игры и дальше не париться


def music_sausage():
    pygame.mixer.music.load('music/ost/Sausage.wav')
    pygame.mixer.music.play(-1)


# Для работы следующей функции необходимо сначала её вызвать, а после прописать такую команду:
# pygame.mixer.music.set_endevent(<Какой-нибудь event>)
# И в цикле игры while прописать:
# if event.type == <Какой-нибудь event>:
#   music_album_of_BTS()


def music_album_of_bts():
    ost = choice(BTS_ALBUM)
    pygame.mixer.music.load(ost)
    pygame.mixer.music.play()


btn_sound = pygame.mixer.Sound('sounds/btn_sound.wav')
win_sound = pygame.mixer.Sound('sounds/win_sound.wav')
konch_sound = pygame.mixer.Sound('sounds/konch_sound.wav')
lose_sound = pygame.mixer.Sound("sounds/lose_sound.wav")
ivan_sound = pygame.mixer.Sound("sounds/ivan_sound.wav")
