import random
import sys
import os
import math
import logging

import pygame
from pygame.locals import *

import combat
import items
import constants as con
import display


def edge_collision_check(pos):
        collision = False
        x, y = pos
        if x < con.GAME_CONSTANTS["MAP_LEFT_EDGE"] or x > con.GAME_CONSTANTS["MAP_RIGHT_EDGE"]:
            collision = True

        elif y < con.GAME_CONSTANTS["MAP_TOP_EDGE"] or y > con.GAME_CONSTANTS["MAP_BOTTOM_EDGE"]:
            collision = True

        return collision


class Hero(object):
    """Contains all the hero specific methods. Keeps track
    of hero position and movements. Will eventually keep
    track of level, skills and abilities, stats, etc.

    Args:
        name (str): Name/description of the hero
        pos (tuple): x/y coordinates of the hero's position (pixel)

    Attributes:
        isalive (bool): Whether the hero is alive or not.
        image_open (pygame Surface): Image (usually png) of the hero
        rect (pygame Rect): Rectangle bounds of player sprite
        inventory (list): List of Item objects the player owns
        hor (int): x coordinate (pixel)
        vert (int): y coordinate (pixel)
    """
    def __init__(self, name, game, pos=(0, 0)):
        self.arrow_keys = {K_LEFT, K_RIGHT, K_UP, K_DOWN}

        self.name = name
        self.isalive = True
        self.last_pos = None
        self.pos = pos

        self.direction = "LEFT"

        self.hor = 0
        self.vert = 0

        self.image = self.set_image(self.direction)
        self.rect = self.update_rect()

        self.inventory_size = con.DIFFICULTY['INVENTORY_SIZE']
        self.inventory = []
        self.coin_purse = 0

        self.mobile = True
        self.collision_on = True
        self.speed = con.DIFFICULTY["HERO_SPEED"]

    def set_pos(self, value):
        self.pos = value
        self.rect = self.update_rect()

    def update(self, game):
        """Manages the players appearance on screen.
        Note that we're not looking for KEYUP. This is because I have
        set the option 'pygame.key.set_repeat()' in main.py, which
        will process multiple KEYDOWN events if a key is held, and
        will repeat at a set interval of milliseconds.
        """
        self.vert = self.hor = 0
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    game.game_over = True

                # logging.debug(event.key)  # WAY too much for regular debugging use
                if event.key == K_LEFT:
                    self.hor -= self.speed
                    self.image = self.set_image("LEFT")
                if event.key == K_RIGHT:
                    self.hor += self.speed
                    self.image = self.set_image("RIGHT")
                if event.key == K_UP:
                    self.vert -= self.speed
                    self.image = self.set_image("UP")
                if event.key == K_DOWN:
                    self.vert += self.speed
                    self.image = self.set_image("DOWN")
                if event.key == K_F11:
                    game.screen.toggle_fullscreen()
                if event.key == K_0:
                    self.toggle_collision()

                if event.key in self.arrow_keys:
                    for enemy in game.level.enemy_sprites:
                        if enemy.isalive and self.mobile:
                            enemy.follow_hero(game, self)

                elif event.key == K_i:
                    inventory_names = [str(item.name) for item in game.hero.inventory]
                    menu_items = [" - Gold - ", str(self.coin_purse)]
                    menu_items.extend(["", "- Inventory -"])
                    menu_items.extend(inventory_names)
                    gm = display.InventoryMenu(game.screen.screen, menu_items)
                    gm.run()

            if event.type == KEYUP and event.key in self.arrow_keys:
                self.start_movement()

        if self.mobile:
            self.move()

        if self.collision_on:
            touched_enemy = pygame.sprite.spritecollideany(self, game.level.enemy_sprites)
            touched_container = pygame.sprite.spritecollideany(self, game.level.container_sprites)
            touched_wall = pygame.sprite.spritecollideany(self, game.level.wall_sprites)
            touched_entity = pygame.sprite.spritecollideany(self, game.level.entity_sprites)
            touched_door = pygame.sprite.spritecollideany(self, game.level.exit_sprites)
            touched_edge = edge_collision_check(self.pos)

            if touched_door:
                self.stop_movement()
                self.set_pos(self.last_pos)
                touched_door.touch(game)
            if touched_enemy:
                self.stop_movement()
                # self.set_pos(self.last_pos
                touched_enemy.touch(self, game)
            if touched_container:
                self.stop_movement()
                self.set_pos(self.last_pos)
                touched_container.touch(self, game)
            if touched_wall or touched_edge:
                self.stop_movement()
                self.set_pos(self.last_pos)
            if touched_entity:
                self.stop_movement()
                if self.rect.colliderect(touched_entity.rect):
                    self.set_pos(self.last_pos)

    def set_image(self, direction):
        try:
            self.direction = direction
            return pygame.image.load(os.path.join(
                con.PATHS["sprites"], "hero_{}.png".format(direction.lower()))
            )
        except ValueError as e:
            error = e.args[0]
            logging.debug('unable to set hero direction. Error: ' + error)
            return pygame.image.load(os.path.join(con.PATHS["sprites"], "hero_down.png"))

    def move(self):
        """Moves the player across the screen."""
        self.last_pos = self.pos

        old_row, old_col = self.pos
        row = old_row + self.hor
        col = old_col + self.vert
        self.set_pos((row, col))
        # self.rect = self.update_rect()

    def toggle_collision(self):
        if self.collision_on:
            self.collision_on = False
        elif not self.collision_on:
            self.collision_on = True
        print(self.collision_on)

    def move_all_monsters(self, game):
        for mob in game.level.enemy_sprites:
            if self.mobile:
                enemy_speed = random.randint(1, 1)
                if enemy_speed == 1:
                    mob_hor = random.randint(-1, 1)
                    mob_vert = random.randint(-1, 1)
                    mob.move(game, mob_hor, mob_vert)

    def update_rect(self):
        """Updates the player rect variable. This needs to happen
        every time the player moves."""
        x, y, = self.pos
        rect = self.image.get_rect(left=x, top=y)
        return rect

    def take_items(self, container):
        """Processes getting contents from chests and corpses"""
        for item in container.contents:
            if item.name == 'gold':
                self.coin_purse += item.amount
                logging.debug('gold is now ' + str(self.coin_purse))

            else:
                if len(self.inventory) <= self.inventory_size:
                    for _ in range(item.amount):
                        self.inventory.append(item)
                    container.drop()
                else:
                    print('inventory full')

    def stop_movement(self):
        self.mobile = False

    def start_movement(self):
        self.mobile = True

    def __getstate__(self):
        state = self.__dict__.copy()

        del state['image']
        # del state['rect']
        # del state['last_pos']

        str_state = str(state)
        logging.debug('saving hero state: ' + str_state)

        return state

    def __setstate__(self, state):
        str_state = str(state)
        logging.debug('loaded hero state" ' + str_state)

        self.__dict__.update(state)

        str_dict = str(self.__dict__)
        logging.debug('after dict update: ' + str_dict)

        self.image = self.set_image(state['direction'])
        # self.rect = self.update_rect()
        self.last_pos = None


class Monster(pygame.sprite.Sprite):
    """Base class all enemy classes will inherit from.
    image_open (pygame Surface): image_open representing the sprite

    Args:
        corpseimage (pygame Surface): image_open when the enemy dies
        drops (list): list of Item objects the corpse will yield
        name (str): Name/description of the enemy
        pos (tuple): x/y coordinates of the enemy

    Attributes:
        image_open (pygame Surface): pygame Surface object represented by image_open
        rect (pygame Rect): rectangle bounds of sprite
        corpse (Container): container object for corpse looting

    """
    def __init__(self, drops, name, pos=(0, 0)):
        pygame.sprite.Sprite.__init__(self)

        self.name = name
        self.isalive = True
        self.pos = pos
        self.last_pos = self.pos
        self.image = self.set_image(self.mob_image)
        self.rect = self.update_rect()
        self.tile = con.GAME_CONSTANTS["TILE"]

        self.corpse = items.Container(self.name, drops)

        self.speed = con.DIFFICULTY["ENEMY_SPEED"]
        self.aggro_dist = con.DIFFICULTY["AGGRO_DIST"]

    def aggro(self, dist):
        if dist < self.aggro_dist * self.tile:
            aggro = True
        else:
            aggro = False

        return aggro

    def touch(self, hero, game):
        """Process events when hero touches enemy objects"""
        if self.isalive:
            if random.randint(0, 9) > 5:
                game.soundplayer.play_sfx('slice_001.wav')
            else:
                game.soundplayer.play_sfx('stab_001.wav')
            combat.Battle.fight(self, hero)
        elif not self.isalive:
            self.loot(hero, game)

    def move(self, game, hor, vert):
        """Moves the monster"""
        if self.isalive:
            self.last_pos = self.pos

            old_col, old_row = self.last_pos

            hor = hor * self.tile
            vert = vert * self.tile

            new_row = old_col + hor
            new_col = old_row + vert

            self.pos = (new_row, new_col)
            # self.rect = self.update_rect()

            self.process_collisions(game)

    def follow_hero(self, game, hero):
        # find normalized direction vector (dx, dy) between enemy and player
        dx, dy = self.rect.x - hero.rect.x, self.rect.y - hero.rect.y
        dist = math.hypot(dx, dy)

        if self.aggro(dist):
            try:
                dx, dy = dx / dist, dy / dist
                self.delta_move(game, dx, dy)
            except ZeroDivisionError:
                pass

    def delta_move(self, game, dx, dy):
        if self.isalive:
            self.last_pos = self.pos

            self.rect.x -= dx * self.speed
            self.rect.y -= dy * self.speed
            self.pos = (self.rect.x, self.rect.y)

        self.process_collisions(game)

    def process_collisions(self, game):
        wall_collision = pygame.sprite.spritecollideany(self, game.level.wall_sprites)
        other_mob_collision = pygame.sprite.spritecollideany(self, game.level.enemy_sprites)
        container_collsion = pygame.sprite.spritecollideany(self, game.level.container_sprites)
        edge_collision = edge_collision_check(self.pos)

        if wall_collision or edge_collision:
            self.pos = self.last_pos
            self.rect = self.update_rect()
        if other_mob_collision:
            if not other_mob_collision == self:
                self.pos = self.last_pos
                self.rect = self.update_rect()
        if container_collsion:
            self.pos = self.last_pos
            self.rect = self.update_rect()

    def update_rect(self):
        """Updates self.rect to current position"""
        x, y, = self.pos
        rect = self.image.get_rect(left=x, top=y)
        return rect

    def die(self):
        self.isalive = False
        self.image = self.set_image(self.corpseimage)
        self.rect = self.update_rect()

    def loot(self, hero, game):
        self.corpse.open(hero)
        self.kill()
        game.blitter.remove(self)

    @staticmethod
    def set_image(image):
        return pygame.image.load(image)

    def __getstate__(self):
        state = self.__dict__.copy()
        del state['image']

        return state

    def __setstate__(self, state):
        state['image'] = self.set_image(os.path.join(con.PATHS["sprites"], "slime.png"))


class Slime(Monster):
    def __init__(self, pos, drops):
        self.mob_image = os.path.join(con.PATHS["sprites"], "slime.png")
        # self.sprite = pygame.sprite.Sprite()
        self.corpseimage = os.path.join(con.PATHS["sprites"], "slimedead.png")
        name = "slime"

        super(Slime, self).__init__(
            drops,
            name,
            pos
        )


class Rat(Monster):
    def __init__(self, pos, drops):
        self.mob_image = os.path.join(con.PATHS["sprites"], "rat.png")
        self.corpseimage = os.path.join(con.PATHS["sprites"], "ratdead.png")
        name = "rat"

        super(Rat, self).__init__(
            drops,
            name,
            pos,
        )


class Ogre(Monster):
    def __init__(self, pos, drops):
        self.mob_image = os.path.join(con.PATHS["sprites"], "ogre1.png")
        self.corpseimage = os.path.join(con.PATHS["sprites"], "ogre1dead.png")
        name = "ogre"

        super(Ogre, self).__init__(
            drops,
            name,
            pos,
        )

    def update_rect(self):
        x, y = self.pos
        if self.isalive:
            return self.image.get_rect(left=x, top=y, height=40, width=20)
        else:
            return self.image.get_rect(left=x, top=y, height=20, width=40)


