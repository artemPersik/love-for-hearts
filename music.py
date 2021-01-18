import pygame
from random import choice

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
BTS_ALBUM = [f"data/music/ost/BTS_{i}.wav" for i in range(10)]

# Это функцию можно вызвать в начале игры и дальше не париться


def music_sausage():
    pygame.mixer.music.load('data/music/ost/Sausage.wav')
    pygame.mixer.music.play(-1)


def set_volume_all_sounds(volume):
    BTN_SOUND.set_volume(volume)
    KONCH_SOUND.set_volume(volume)
    WIN_SOUND.set_volume(volume)
    LOSE_SOUND.set_volume(volume)
    IVAN_SOUND.set_volume(volume)
    pygame.mixer.music.set_volume(volume)


# Для работы следующей функции необходимо сначала её вызвать, а после прописать такую команду:
# pygame.mixer.music.set_endevent(<Какой-нибудь event>)
# И в цикле игры while прописать:
# if event.type == <Какой-нибудь event>:
#   music_album_of_BTS()


def music_album_of_bts():
    ost = choice(BTS_ALBUM)
    pygame.mixer.music.load(ost)
    pygame.mixer.music.play()


BTN_SOUND = pygame.mixer.Sound('data/music/sounds/btn_sound.wav')
WIN_SOUND = pygame.mixer.Sound('data/music/sounds/win_sound.wav')
KONCH_SOUND = pygame.mixer.Sound('data/music/sounds/konch_sound.wav')
LOSE_SOUND = pygame.mixer.Sound("data/music/sounds/lose_sound.wav")
IVAN_SOUND = pygame.mixer.Sound("data/music/sounds/ivan_sound.wav")
