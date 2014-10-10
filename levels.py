import random

__author__ = "micah turner"

import os
import logging

import pygame

import characters
import items
import entities
import constants as con


def parse_pos(pos):
    tile = con.GAME_CONSTANTS["TILE"]
    x, y = pos
    ox, oy = con.DISPLAY["VIEWFRAME_OFFSET"]

    # Adjust for tile size
    x = x * tile
    y = y * tile

    # Adjust for screen position offset
    x += ox
    y += oy

    parsed_position = (x, y)

    return parsed_position


class Level(pygame.sprite.Sprite):
    def __init__(self, name, wall_image, isle_image, start_pos, game):
        self.name = name

        self.image = pygame.image.load(
            os.path.join(con.PATHS['backgrounds'], self.mapimage))
        self.mapfile = os.path.join(con.PATHS['maps'], self.name + ".map")

        self.tile = con.GAME_CONSTANTS["TILE"]
        self.startpos = start_pos

        top_left_corner = parse_pos((0, 0))
        self.pos = top_left_corner

        self.enemy_sprites = pygame.sprite.Group()
        self.container_sprites = pygame.sprite.Group()
        self.exit_sprites = pygame.sprite.Group()
        self.entity_sprites = pygame.sprite.Group()
        self.wall_sprites = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()

        self.wall_image = wall_image
        self.isle_image = isle_image

        self.parse_map()

        self.all_sprites.add(
            self.wall_sprites,
            self.enemy_sprites,
            self.container_sprites,
            self.entity_sprites)

        for sprite in self.all_sprites:
            game.blitter.register(sprite, self.name, layer=2)
        game.blitter.register(self, self.name, layer=1)
        game.blitter.register(game.hero, self.name, layer=3)

        game.explored_areas.append(self)

    def parse_map(self):
        x, y = con.GAME_CONSTANTS["MAP_TOP_LEFT"]

        wall = "W"
        isle = "I"
        hero = "H"
        chest = "c"
        slime = "s"
        rat = "r"
        ogre = "O"
        torch = "t"
        throne = "T"

        with open(os.path.join(self.mapfile), "r") as level_map:
            for row in level_map:
                for tile in row:
                    if tile == wall:
                        new_wall = entities.Wall((x, y), self.wall_image)
                        self.wall_sprites.add(new_wall)

                    elif tile == isle:
                        new_isle = entities.Isle((x, y), self.isle_image)
                        self.wall_sprites.add(new_isle)

                    elif tile == hero:
                        self.startpos = (x, y)

                    elif tile == chest:
                        item_amount = random.randint(1, 3)  # from 1 to 3 items
                        gold_value = random.randint(1, 33)
                        item_pool = (
                            items.SlimeDust(item_amount),
                            items.RatTail(item_amount),
                            items.Bone(item_amount))
                        choice = random.randint(0, len(item_pool)-1)

                        new_chest = items.Chest(
                            pos=(x, y),
                            contents=[
                                item_pool[choice],
                                items.Gold(gold_value),
                            ]
                        )
                        self.container_sprites.add(new_chest)

                    elif tile == slime:
                        new_slime = characters.Slime(
                            pos=(x, y),
                            drops=[items.SlimeDust(1)])
                        self.enemy_sprites.add(new_slime)

                    elif tile == rat:
                        new_rat = characters.Rat(
                            pos=(x, y),
                            drops=[items.RatTail(1)])
                        self.enemy_sprites.add(new_rat)

                    elif tile == ogre:
                        new_ogre = characters.Ogre(
                            pos=(x, y),
                            drops=[items.Bone(1)])
                        self.enemy_sprites.add(new_ogre)

                    elif tile == torch:
                        new_torch = entities.Torch((x, y))
                        self.entity_sprites.add(new_torch)

                    elif tile == throne:
                        new_throne = entities.Throne((x, y))
                        self.entity_sprites.add(new_throne)

                    x += self.tile

                y += self.tile
                x = self.tile

    def __getstate__(self):
        state = self.__dict__.copy()
        del state['image']

        str_state = str(state)
        logging.error('saving level: ' + str_state)
        logging.error('wtf')
        return state

    def __setstate__(self, state):
        state['image'] = pygame.image.load(os.path.join(con.PATHS['backgrounds'], self.mapimage))
        self.__dict__.update(state)


class Start(Level):
    def __init__(self, game):
        name = "Start"
        self.mapimage = "greyfloor.png"
        wall_image = "wall1.png"
        isle_image = "emptyisle.png"
        start_pos = parse_pos((14, 19))
        self.ambient_volume = 0.2
        self.bgm = 'engine_slow.wav'

        super(Start, self).__init__(name, wall_image, isle_image, start_pos, game)

        self.northdoor1 = items.Door(
            dest_level="Isle2",
            pos=parse_pos((14, 0)),
            dest_startpos=parse_pos((14, 19)),
        )
        self.exit_sprites.add(self.northdoor1)
        for door in self.exit_sprites:
            game.blitter.register(door, self.name, layer=2)


class Isle2(Level):
    def __init__(self, game):
        name = "Isle2"
        self.mapimage = "greyfloor.png"
        wall_image = "wall1.png"
        isle_image = "emptyisle.png"
        start_pos = parse_pos((14, 19))
        self.ambient_volume = 0.3
        self.bgm = 'engine_slow.wav'

        super(Isle2, self).__init__(name, wall_image, isle_image, start_pos, game)

        self.southdoor1 = items.Door(
            dest_level="Start",
            pos=parse_pos((14, 20)),
            dest_startpos=parse_pos((14, 1)),
        )
        self.northdoor1 = items.Door(
            dest_level="ThroneRoom",
            pos=parse_pos((14, 0)),
            dest_startpos=parse_pos((14, 19)),
        )
        self.exit_sprites.add(self.southdoor1, self.northdoor1)

        for door in self.exit_sprites:
            game.blitter.register(door, self.name, layer=2)


class ThroneRoom(Level):
    def __init__(self, game):
        name = "ThroneRoom"
        self.mapimage = "dark_gray_floor.png"
        wall_image = "wall1.png"
        isle_image = "emptyisle.png"
        start_pos = parse_pos((14, 19))
        self.ambient_volume = .4
        self.bgm = 'engine_slow.wav'

        super(ThroneRoom, self).__init__(name, wall_image, isle_image, start_pos, game)

        self.southdoor1 = items.Door(
            dest_level="Isle2",
            pos=parse_pos((14, 20)),
            dest_startpos=parse_pos((14, 1)),
        )
        self.exit_sprites.add(self.southdoor1)
        for door in self.exit_sprites:
            game.blitter.register(door, self.name, layer=2)


def choose_level(levelname, game):
    if levelname == "Isle2":
        room = Isle2(game)
    elif levelname == "Start":
        room = Start(game)
    elif levelname == "ThroneRoom":
        room = ThroneRoom(game)
    else:
        return False

    if not room.bgm == game.current_bgm:
        logging.debug('current bgm was: ' + game.current_bgm + ' room bgm is: ' + room.bgm)
        game.soundplayer.play_bgm(room.bgm)
        game.current_bgm = room.bgm

    game.soundplayer.set_bgm_volume(room.ambient_volume)
    return room


def teleport(levelname, game):
    for area in game.explored_areas:
        area_name = str(area.name)

        if levelname == area_name:
            game.soundplayer.set_bgm_volume(area.ambient_volume)

            return area

    #  Or, if the room hasn't already been visited by the player, instantiate it
    return choose_level(levelname, game)