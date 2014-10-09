__author__ = 'micaht'

import os

import pygame

import constants as con


class Entity(pygame.sprite.Sprite):
    def __init__(self, name, pos, image):
        pygame.sprite.Sprite.__init__(self)

        self.name = name
        self.pos = pos
        self.image = self.set_image(image)
        self.rect = self.update_rect()

    @staticmethod
    def set_image(image):
        return pygame.image.load(image)

    def update_rect(self):
        x, y = self.pos
        return self.image.get_rect(top=y, left=x)


class Wall(Entity):
    def __init__(self, pos, wall_image):
        x, y = pos
        name = "Wall({}x{})".format(x, y)
        image = os.path.join(con.PATHS['entities'], wall_image)
        super(Wall, self).__init__(name, pos, image)


class Isle(Entity):
    def __init__(self, pos, isle_image):
        x, y = pos
        name = "Isle({}x{})".format(x, y)
        image = os.path.join(con.PATHS['entities'], isle_image)
        super(Isle, self).__init__(name, pos, image)

    def update_rect(self):
        x, y = self.pos
        return self.image.get_rect(top=y, left=x, width=20, height=20)


class Torch(Entity):
    def __init__(self, pos):
        x, y = pos
        name = "Torch({}x{})".format(x, y)
        image = os.path.join(con.PATHS['entities'], "torch1.png")

        super(Torch, self).__init__(name, pos, image)


class Throne(Entity):
    def __init__(self, pos):
        x, y = pos
        name = "Throne1({}x{})".format(x, y)
        image = os.path.join(con.PATHS['entities'], "throne1.png")

        super(Throne, self).__init__(name, pos, image)