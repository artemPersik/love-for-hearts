import pygame
import random
import os
import sys
from PIL import Image

# стартовые переменны и дебаг мод
FPS = 60
otlad = 1
all_sprites = pygame.sprite.Group()
if otlad == 1:
    size = width, height = 1920, 1080
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    screen = pygame.display.set_mode(size, pygame.RESIZABLE)
else:
    size = width, height = 800, 800
    screen = pygame.display.set_mode(size)

music = ["BTS - Dynamite.mp3"]


class Game_objects:
    def __init__(self):
        pass

    # не лезь сюда :) если интересно см учебник
    def load_image(self, name, colorkey=None):
        fullname = os.path.join('data/images/', name)
        try:
            image = pygame.image.load(fullname)
        except pygame.error as message:
            print('Cannot load image:', name)
            raise SystemExit(message)
        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
        else:
            image = image.convert_alpha()
        return image

    # функция что бы картинки выводились
    def my_sprite(self, name, X, Y, colorkey=None):
        # имя картинки с расширением, кординаты, это если картинка на каком то фоне, то оно его сделает прозрачным
        all_sprites = pygame.sprite.Group()
        sprite = pygame.sprite.Sprite()
        sprite.image = Game_objects().load_image(name, colorkey)
        sprite.rect = sprite.image.get_rect()
        all_sprites.add(sprite)
        sprite.rect.x = X
        sprite.rect.y = Y
        all_sprites.draw(screen)

    def render(self, x, y, image1=None, image2=None, action=None):
        # корды, картика в простой форме, картинка при наведении, функция
        if image1 is None:
            width, height = 100, 100
        else:
            im = Image.open(f"data/images/{image1}")
            (width, height) = im.size

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x < mouse[0] < x + width and y < mouse[1] < y + height:
            if image2 is not None:
                Game_objects().my_sprite(image2, x, y)
            if click[0] == 1:
                if action is not None:
                    eval(action)
                else:
                    pass
                pygame.time.delay(300)
        else:
            if image2 is not None:
                Game_objects().my_sprite(image1, x, y)

    def music(self):
        sound = music[random.randint(0, len(music)) - 1]
        fullname = os.path.join('data/music/', sound)
        return fullname


# это будет класс с эффектами
class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


class Scene_objects:
    def __init__(self):
        pass

    # тут лежат кнопочки для менюшки
    def scene_buttons(self):
        go.render(70, 65, "new game.png", "new game2.png")
        go.render(70, 265, "continue.png", "continue2.png")
        go.render(70, 465, "options.png", "options2.png")
        go.render(70, 665, "authors.png", "authors2.png")
        go.render(70, 865, "quit.png", "quit2.png", "quit()")
        go.my_sprite("para2.png", 900, 53)


if __name__ == '__main__':
    #
    pygame.init()
    running = True
    go = Game_objects()
    so = Scene_objects()

    clock = pygame.time.Clock()
    heart = AnimatedSprite(go.load_image("heart.png"), 6, 2, 1100, 53)
    music1 = pygame.mixer.Sound(go.music())
    music1.play(100)

    while running:
        for event in pygame.event.get():
            # при закрытии окна
            if event.type == pygame.QUIT:
                running = False
        screen.fill("#DF1479")
        so.scene_buttons()
        all_sprites.draw(screen)
        all_sprites.update()
        clock.tick(FPS)
        pygame.display.flip()
    pygame.display.flip()
    pygame.quit()
