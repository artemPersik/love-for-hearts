from constants import CHARACTERS
from music import BTN_SOUND, set_volume_all_sounds
import pygame


# Группа для всех спрайтов, с выводом слайдера и курсора поверх других изображений
class AllSprites(pygame.sprite.Group):
    def draw(self, surface):
        sprites = self.sprites()
        surface_blit = surface.blit
        sprites.sort(key=lambda x: isinstance(x, Slider))
        sprites.sort(key=lambda x: isinstance(x, Cursor))
        for spr in sprites:
            self.spritedict[spr] = surface_blit(spr.image, spr.rect)
        self.lostsprites = []


# Клас курсора, ничего интересного)))
class Cursor(pygame.sprite.Sprite):
    def __init__(self, screen, image):
        self.group = pygame.sprite.Group()
        super().__init__(self.group)
        self.image = image
        self.rect = self.image.get_rect()
        self.screen = screen

    def update(self):
        if pygame.mouse.get_focused():
            self.rect.x, self.rect.y = pygame.mouse.get_pos()
            self.group.draw(self.screen)


class StaticImage(pygame.sprite.Sprite):
    def __init__(self, groups, image, pos_x, pos_y):
        super().__init__(*groups)
        self.image = image
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.groups = groups

    def move_to(self, pos):
        self.rect.x, self.rect.y = pos


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, groups, sheet, columns, rows, x, y):
        super().__init__(*groups)
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


# Класс кнопки
class Button(pygame.sprite.Sprite):
    # Ну тут тупа генератор, по названию переменных всё очевидно)
    def __init__(self, pos_x, pos_y, width, height, pass_image, direct_image, clicked_image,
                 groups, cursor, func, is_visible=True):
        super().__init__(*groups)

        self.pass_image = pygame.transform.scale(pass_image, (width, height))
        self.direct_image = pygame.transform.scale(direct_image, (width, height))
        self.clicked_image = pygame.transform.scale(clicked_image, (width, height))
        self.image = self.pass_image
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.mask = pygame.mask.from_surface(self.image)
        self.is_visible = is_visible
        self.groups = groups
        self.pos = (pos_x, pos_y)
        self.cursor = cursor
        self.func = func
        self.width, self.height = width, height
        self.is_clicked = False

    # Ну типа проверка нажатий и наведений на кнопку
    def update(self, *events):
        if not self.is_visible:
            return

        # проверка на на отпускае мыши
        if self.is_clicked and self.is_mouse_button_up(events[0]):
            self.image = self.clicked_image
            BTN_SOUND.play()
            if self.func is not None:
                self.func()
            self.is_clicked = False
        # проверка на нажатие мыши
        elif self.is_mouse_button_down():
            self.image = self.clicked_image
        # проверка на наведение мыши на кнопку
        elif self.is_direct():
            self.image = self.direct_image
        else:
            self.image = self.pass_image
        self.update_is_clicked(events[0])

    def update_is_clicked(self, event):
        if event and event.type == pygame.MOUSEBUTTONUP:
            self.is_clicked = False
        elif event and event.type == pygame.MOUSEBUTTONDOWN and pygame.sprite.collide_mask(self, self.cursor):
            self.is_clicked = True

    # Проверка на на отпускае мыши
    def is_direct(self):
        return not pygame.mouse.get_pressed(3)[0] and pygame.sprite.collide_mask(self, self.cursor)

    # Проверка на нажатие мыши
    def is_mouse_button_down(self):
        if pygame.mouse.get_pressed(3)[0] and pygame.sprite.collide_mask(self, self.cursor):
            return True
        return False

    # Проверка на на отпускае мыши
    def is_mouse_button_up(self, event):
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and pygame.sprite.collide_mask(self, self.cursor):
            return True
        return False

    # Куча методов для изменения и получения переменных экземпляра класса
    def get_pos(self):
        return self.pos

    def get_pos_x(self):
        return self.pos[0]

    def get_pos_y(self):
        return self.pos[1]

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_func(self):
        return self.func

    def set_pass_image(self, image):
        self.pass_image = image

    def set_direct_image(self, image):
        self.direct_image = image

    def set_clicked_image(self, image):
        self.clicked_image = image

    def set_pos(self, pox_x, pos_y):
        self.pos = (pox_x, pos_y)
        self.rect.x, self.rect.y = self.get_pos()

    def set_width(self, width):
        self.width = width
        self.rect.width = self.get_width()

    def set_height(self, height):
        self.height = height
        self.rect.height = self.get_height()

    def set_func(self, func):
        self.func = func

    def set_visible(self, value):
        if value and all(self not in group for group in self.groups):
            for group in self.groups:
                group.add(self)
        if not value and all(self in group for group in self.groups):
            for group in self.groups:
                group.remove(self)


# Класс для ползунка у слайдера
class Slider(pygame.sprite.Sprite):
    def __init__(self, image, groups, size=None, pos=None):
        super().__init__(*groups)
        if size is not None:
            image = pygame.transform.scale(image, size)
        self.image = image
        self.rect = self.image.get_rect()
        self.groups = groups
        if pos is not None:
            self.rect.x, self.rect.y = pos

    def move(self, x, y):
        self.rect.x += x
        self.rect.y += y


# Класс для слайдера громкостти
class VolumeSlider(pygame.sprite.Sprite):
    def __init__(self, pos, line_image, line_size, size, slider, groups, volume):
        super().__init__(*groups)
        self.image = pygame.transform.scale(line_image, line_size)
        self.rect = self.image.get_rect().move(pos[0], pos[1] + (size[1] - line_size[1]) // 2)
        self.volume_slider = pygame.Rect(*pos, *size)
        self.slider, self.volume, self.flag = slider, volume, False
        self.slider.rect.x, self.slider.rect.y = size[0] * volume + pos[0] - slider.rect.width // 2, pos[1]

        self.groups = groups
        self.pos_x, self.pos_y = pos
        self.width, self.height = size
        self.slider_width, self.slider_height = self.rect.size

    # Метод для того, чтобы ползунок не уходил дальше положенного
    def fix_slider_coord(self):
        if self.slider.rect.x < self.rect.x - self.slider.rect.width // 2:
            self.slider.rect.x = self.rect.x - self.slider.rect.width // 2
        elif self.slider.rect.x > self.rect.x + self.rect.width - self.slider.rect.width // 2:
            self.slider.rect.x = self.rect.x + self.rect.width - self.slider.rect.width // 2

    # Метод для движения ползунка по слайдеру
    def update(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.volume_slider.collidepoint(event.pos):
            self.slider.rect.x = event.pos[0] - self.slider.rect.width // 2
            self.flag = True

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.flag = False

        if event.type == pygame.MOUSEMOTION and self.flag:
            self.slider.rect.x += event.rel[0]
            self.fix_slider_coord()

        if event.type == pygame.MOUSEWHEEL:
            self.slider.rect.x += event.y * self.slider.rect.width // 20
            self.fix_slider_coord()
        self.volume = round((self.slider.rect.x - self.rect.x + self.slider.rect.width // 2) / self.rect.width, 2)
        set_volume_all_sounds(self.volume)

    # Метод для получения громкости
    def get_volume(self):
        return self.volume


class ScrollBox:
    def __init__(self, pos_x, pos_y, width, height, text_x, text_y, buttons, visible_count, indent, slider=None):
        self.pos_x, self.pos_y, self.width, self.height = pos_x, pos_y, width, height
        self.text_x, self.text_y = text_x, text_y
        self.rect = pygame.Rect(pos_x, pos_y, width, height)
        self.buttons, self.indent = buttons, indent
        self.visible_count, self.ind = visible_count, 0
        self.visible_buttons = self.buttons[self.ind:self.ind + self.visible_count]
        self.characters_values = [item for value in CHARACTERS.values() for item in value]
        self.collection = []
        self.slider = slider

        self.update_buttons()

    def update(self, *events):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if events[0] and events[0].type == pygame.MOUSEWHEEL:
                self.ind -= events[0].y
                if self.slider is not None:
                    rel_y = (self.height - self.slider.rect.height) * events[0].y / (len(self.buttons) - 1)
                    self.slider.move(0, -rel_y)
                    if self.slider.rect.y > self.pos_y - self.slider.rect.height * 1.25 + self.height:
                        self.slider.rect.y = self.pos_y - self.slider.rect.height * 1.25 + self.height
                    if self.slider.rect.y < self.pos_y + self.slider.rect.height * 0.25:
                        self.slider.rect.y = self.pos_y + self.slider.rect.height * 0.25

                if self.ind < 0:
                    self.ind = 0
                if self.ind > len(self.characters_values) - self.visible_count:
                    self.ind = len(self.characters_values) - self.visible_count
            if events[0] and events[0].type == pygame.KEYUP and events[0].key == pygame.K_BACKSPACE:
                if self.collection:
                    del self.collection[-1]
            self.update_buttons()

    def update_buttons(self):
        self.visible_buttons = self.buttons[self.ind:self.ind + self.visible_count]
        for i, button in enumerate(self.buttons):
            button.set_func(lambda x=self.characters_values[i]: self.collection.append(x)
                if len(self.collection) < 5 and x not in self.collection else 0)
            if button in self.visible_buttons:
                button.set_visible(True)
                button.set_pos(self.pos_x, self.pos_y + self.indent * (i - self.ind))
            else:
                button.set_visible(False)
                button.set_pos(2000, 0)

    def render(self, screen, color, font, symbols_on_line, indent):
        text = ', '.join(self.collection).capitalize()
        pos_x, pos_y = self.text_x, self.text_y
        intro_text = []
        line = ''

        for i, word in enumerate(text.split()):
            if len(line) + len(word) <= symbols_on_line:
                line += f' {word}'
            else:
                intro_text.append(line[1:])
                line = f' {word}'

            if i == len(text.split()) - 1:
                intro_text.append(line[1:])

        for line in intro_text:
            string_rendered = font.render(line, 1, color)
            intro_rect = string_rendered.get_rect()
            pos_y += indent
            intro_rect.top = pos_y
            intro_rect.x = pos_x
            pos_y += intro_rect.height
            screen.blit(string_rendered, intro_rect)

    def get_collection(self):
        return self.collection

    def set_collection(self, collection):
        self.collection = collection


class SpinBox:
    def __init__(self, pos_x, pos_y, width, height):
        self.pos_x, self.pos_y, self.width, self.height = pos_x, pos_y, width, height
        self.rect = pygame.rect.Rect(pos_x, pos_y, width, height)
        self.flag = False
        self.value = ''

    def update(self, *events):
        pos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed(3)
        if self.rect.collidepoint(pos) and click[0]:
            self.flag = True
        elif not self.rect.collidepoint(pos) and click[0]:
            self.flag = False

        if self.flag:
            if events[0].type == pygame.KEYDOWN:
                if events[0].key == pygame.K_BACKSPACE:
                    self.value = self.value[0:-1]
                if len(self.value) < 2:
                    if events[0].unicode in [str(i) for i in range(10)]:
                        self.value += events[0].unicode

    def render(self, screen, color, font):
        string_rendered = font.render(self.value, 1, color)
        intro_rect = string_rendered.get_rect()
        intro_rect.top = self.pos_y
        intro_rect.x = self.pos_x + self.width // 2 - intro_rect.width // 2
        screen.blit(string_rendered, intro_rect)

    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = value

