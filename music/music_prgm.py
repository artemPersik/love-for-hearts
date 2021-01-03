import pygame

from random import choice

BTS_ALBUM = [f"music/ost/BTS_{i}.wav" for i in range(10)]

# Это функцию можно вызвать в начале игры и дальше не париться


def music_sausage():
    pygame.mixer.music.load('music/ost/Sausage.wav')
    pygame.mixer.music.play(-1)


# Для работы данной функции необходимо сначала её вызвать, а после прописать такую команду:
# pygame.mixer.music.set_endevent(<Какой-нибудь event>)
# И в цикле игры while прописать:
# if event.type == <Какой-нибудь event>:
#   music_album_of_BTS()
# Чуть позже рассмотрю возможность создания собственных event-ов(BTS_event)


def music_album_of_bts():
    ost = choice(BTS_ALBUM)
    pygame.mixer.music.load(ost)
    pygame.mixer.music.play()
