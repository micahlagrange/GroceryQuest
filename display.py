__author__ = "micah turner"

import pygame
from pygame.locals import *

import logging

import constants as con


class ScreenInit(object):
    def __init__(self):
        pygame.display.init()
        self.fullscreen = con.DISPLAY["FULLSCREEN"]

        screendepth = 24
        self.size = self.choose_size()
        self.bestdepth = self.mode_ok(self.size, screendepth)
        self.screen = self.set_mode(self.size, 0, self.bestdepth)
        pygame.display.set_caption(con.GAME_CONSTANTS["GAME_TITLE"])

    @staticmethod
    def set_mode(resolution, flags, depth):
        return pygame.display.set_mode(resolution, flags, depth)


    @staticmethod
    def mode_ok(size, flags=0, depth=0):
        return pygame.display.mode_ok(size, flags, depth)

    @staticmethod
    def choose_size():
        return con.DISPLAY["RESOLUTION"]

    def toggle_fullscreen(self):
        curr_size = self.size
        curr_depth = self.bestdepth

        if self.fullscreen == 0:
            self.fullscreen = FULLSCREEN

        elif self.fullscreen == FULLSCREEN:
            self.fullscreen = 0

        self.screen = self.set_mode(curr_size, self.fullscreen, curr_depth)


class BlitManager():
    def __init__(self, screen):
        self.screen = screen
        self.blit_registry = {}

    # blit all layers one at a time
    def blit_all(self, level):
        self.blit(1, level)
        self.blit(2, level)
        self.blit(3, level)

    # add an item to the blit queue
    def register(self, surface, roomname, layer):
        self.blit_registry[surface] = {"layer": layer, "room": roomname}

    def remove(self, surface):
        del self.blit_registry[surface]

    # blit all surfaces in specified layer
    def blit(self, blitting_layer, level):
        for surface, surface_data in self.blit_registry.items():
            if surface_data["layer"] == blitting_layer and surface_data["room"] == level.name:
                self.screen.blit(surface.image, surface.pos)

    def change_layer(self, surface, new_layer):
        if surface in self.blit_registry.keys():
            self.blit_registry[surface]["layer"] = new_layer

    def change_room(self, surface, new_room):
        if surface in self.blit_registry.keys():
            self.blit_registry[surface]["room"] = new_room.name

    def print_queue(self):
        queue = ''
        for surface in self.blit_registry.keys():
            surface_data = self.blit_registry[surface]
            queue += surface.name + ', layer ' + str(surface_data["layer"]) + 'room: ' + surface_data["room"] + '; '

        return queue

    # def __getstate__(self):
    #     state = self.__dict__.copy()
    #     # del state['screen']
    #
    #     return state
    #
    # def __setstate__(self, state):
    #     self.__dict__.update(state)


class Button():
    def __init__(self):
        pass


class InventoryMenu():
    def __init__(
            self, screen, items, bg_color=con.COLORS['BLACK'],
            font=None, font_size=con.PREFERENCES["MENU_FONT_SIZE"],
            font_color=con.COLORS['BLUE']
    ):
        self.screen = screen
        self.scr_width = self.screen.get_rect().width
        self.scr_height = self.screen.get_rect().height

        self.bg_color = bg_color
        self.clock = pygame.time.Clock()

        self.items = []

        for index, item in enumerate(items):
            menu_item = MenuItem(item, font, font_size, font_color)  # , '/home/nebelhom/.fonts/SHOWG.TTF')

            text_height = len(items) * menu_item.height
            pos_x = (self.scr_width / 2) - (menu_item.width / 2)
            # This line includes a bug fix by Ariel (Thanks!)
            # Please check the comments section for an explanation
            pos_y = (self.scr_height / 2) - (text_height / 2) + ((index * 2) + index * menu_item.height)

            menu_item.set_position(pos_x, pos_y)
            self.items.append(menu_item)

    def run(self):
        mainloop = True
        while mainloop:
            for event in pygame.event.get():
                if event.type == KEYUP: 
                    if event.type == pygame.QUIT or event.key in [pygame.K_i, pygame.K_ESCAPE]:
                        mainloop = False

            # Redraw the background
            self.screen.fill(self.bg_color)

            for item in self.items:
                mouse_pos = pygame.mouse.get_pos()
                lmb_clicked = pygame.mouse.get_pressed()[0]

                mousex, mousey = mouse_pos
                if item.is_mouse_selection(mousex, mousey):
                    item.set_font_color(con.COLORS["RED"])
                    item.set_italic(True)
                    if lmb_clicked:
                        logging.debug('mouseclick syntax still unwritten')
                else:
                    item.set_font_color(con.COLORS["WHITE"])
                    item.set_italic(False)
                self.screen.blit(item.label, item.position)

            pygame.display.flip()


class MenuItem(pygame.font.Font):
    def __init__(
            self,
            text,
            font=None,
            font_size=con.PREFERENCES["MENU_FONT_SIZE"],
            font_color=con.COLORS['BLUE'],
            pos_x=0,
            pos_y=0):
        pygame.font.Font.__init__(self, font, font_size)
        self.text = text
        self.font_size = font_size
        self.font_color = font_color
        self.label = self.render(self.text, 1, self.font_color)
        self.width = self.label.get_rect().width
        self.height = self.label.get_rect().height
        self.dimensions = (self.width, self.height)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.position = pos_x, pos_y

    def set_position(self, x, y):
        self.position = (x, y)
        self.pos_x = x
        self.pos_y = y

    def set_font_color(self, rgb_tuple):
        self.font_color = rgb_tuple
        self.label = self.render(self.text, 1, self.font_color)

    def is_mouse_selection(self, posx, posy):
        if self.pos_x <= posx <= self.pos_x + self.width:
            if self.pos_y <= posy <= self.pos_y + self.height:
                return True
        return False