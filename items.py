__author__ = "micah turner"

import os
import logging

import pygame

import levels
import constants as con


class Door(pygame.sprite.Sprite):
    def __init__(self, dest_level, pos, dest_startpos):
        pygame.sprite.Sprite.__init__(self)
        self.pos = pos
        self.dest_level = dest_level
        self.dest_startpos = dest_startpos

        self.image = self.set_image(os.path.join(con.PATHS['sprites'], "door1.png"))
        self.image_open = os.path.join(con.PATHS['sprites'], "door1open.png")
        self.rect = self.update_rect()

        self.name = 'Door({})'.format(self.pos)

        self.is_open = False

    def touch(self, game):

        self.open_door(game)
        self.rect = self.update_rect()
        moveto_level = levels.teleport(
            self.dest_level, game
        )
        game.level = moveto_level
        game.hero.pos = self.dest_startpos
        game.blitter.change_room(game.hero, game.level)

    @staticmethod
    def set_image(imagefile):
        image = pygame.image.load(imagefile)
        return image

    def update_rect(self):
        x, y = self.pos
        rect = self.image.get_rect(left=x, top=y)
        return rect

    def open_door(self, game):
        if not self.is_open:
            self.is_open = True
            self.image = self.set_image(self.image_open)
            game.soundplayer.play_sfx('door_open.wav')


class Container(pygame.sprite.Sprite):
    def __init__(self, name, contents):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.contents = contents

    def describe_item(self):
        for item, description in self.contents:
            logging.debug(item.name + item.description)

    def open(self, hero):
        if self.contents:
            hero.take_items(self)
            return True
        else:
            return None

    def drop(self):
        self.contents = []


class Chest(Container):
    def __init__(self, pos, contents):
        self.chest_closed_img = os.path.join(con.PATHS['sprites'], "chest1.png")
        self.chest_open_img = os.path.join(con.PATHS['sprites'], "chest1open.png")
        self.image = self.set_image(self.chest_closed_img)
        self.pos = pos
        rx, ry = self.pos
        self.rect = self.image.get_rect(top=ry, left=rx)
        name = "chest({}x{})".format(rx, ry)
        self.open_state = 0

        super(Chest, self).__init__(name, contents)

    def touch(self, hero, game):
        if not self.open_state:
            if self.open(hero):
                self.image = self.set_image(self.chest_open_img)
                self.open_setter()
                game.soundplayer.play_sfx('loose_change.wav')
            else:
                hero.pos = hero._last_pos

    def open_setter(self):
        self.open_state = 1

    def __str__(self):
        ret = ""
        for item in self.contents:
            item = str(item)
            ret += item + str(" received.")
        return ret

    @staticmethod
    def set_image(image):
        return pygame.image.load(image)


class Item(object):
    def __init__(self, name, description, amount):
        self.name = name
        self.amount = amount
        self.description = description

    def count(self):
        logging.debug(self.amount + self.name)


class Gold(Item):
    def __init__(self, amount):
        name = "gold"
        description = "Money, money, money"
        super(Gold, self).__init__(name, description, amount)


class RatTail(Item):
    def __init__(self, amount):
        name = "Rat tail"
        description = "Why would you pick that up?"
        super(RatTail, self).__init__(name, description, amount)


class SlimeDust(Item):
    def __init__(self, amount):
        name = "Slime dust"
        description = "Icky. Gooey."
        super(SlimeDust, self).__init__(name, description, amount)


class Bone(Item):
    def __init__(self, amount):
        name = "Bone"
        description = "Large and heavy bone."
        super(Bone, self).__init__(name, description, amount)