import sys

__author__ = "micah turner"

import logging
import pickle
import os

import pygame
from pygame.locals import *

import constants as con
import display
import characters
import levels
import sound


class LoadGame():
    def __init__(self, hero_name):
        self.level_save_path = os.path.join(con.PATHS['save_dir'], 'levels')
        self.hero_name = hero_name
        self.hero_savefile = os.path.join(con.PATHS['save_dir'], 'hero')
        self.blit_reg_savefile = os.path.join(con.PATHS['save_dir'], 'blit_registry')

    def load_hero(self, game):
        if not os.path.exists(self.hero_savefile):
            hero = characters.Hero(name=self.hero_name, pos=(0, 0))

        else:
            with open(self.hero_savefile, 'rb') as savefile:
                hero = pickle.load(savefile)
                game.start_levelname = hero.current_level

        return hero

    def save_hero(self, hero):
        with open(self.hero_savefile, 'wb') as hero_save_path:
            pickle.dump(hero, hero_save_path)

    def load_levels(self):
        if os.path.exists(self.level_save_path):
            logging.debug('loading level path ' + self.level_save_path)
            with open(self.level_save_path, 'rb') as level_load_path:
                level = pickle.load(level_load_path)
        else:
            level = []

        return level

    def save_levels(self, level_list):
        with open(self.level_save_path, 'wb') as level_save_path:
            pickle.dump(level_list, level_save_path)

    def load_blit_registry(self):
        if os.path.exists(self.blit_reg_savefile):
            with open(self.blit_reg_savefile, 'rb') as blit_loadfile:
                blit_registry = pickle.load(blit_loadfile)
        else:
            blit_registry = {}

        return blit_registry

    def save_blit_registry(self, registry):
        with open(self.blit_reg_savefile, 'wb') as blit_savefile:
            pickle.dump(registry, blit_savefile)

    def load_hero_pos(self, game):
        if os.path.exists(self.hero_savefile):
            pass
        else:
            game.hero.pos = game.level.startpos


class Game(object):
    def __init__(self, levelname, hero_name=con.PREFERENCES["HERO_NAME"]):
        self.events = []
        self.game_over = False
        self.game_loader = LoadGame(hero_name)

        pygame.init()

        if con.PREFERENCES["KEY_REPEAT_ON"]:
            pygame.key.set_repeat(
                con.PREFERENCES["KEY_DELAY"],
                con.PREFERENCES["KEY_REPEAT"],
            )
        logging.debug('key repetition is set to ' + str(con.PREFERENCES['KEY_REPEAT_ON']))

        self.fpsClock = pygame.time.Clock()

        self.screen = display.ScreenInit()
        self.blitter = display.BlitManager(self.screen.screen)
        self.soundplayer = sound.SoundPlayer()

        self.start_levelname = levelname
        self.explored_areas = self.game_loader.load_levels()
        self.current_bgm = ''

        self.hero = self.game_loader.load_hero(self)
        self.blitter.blit_registry = self.game_loader.load_blit_registry()

        self.level = levels.choose_level(self.start_levelname, self)
        self.game_loader.load_hero_pos(self)

    def get_events(self):
        self.events = pygame.event.get()


def main():
    game = Game('Start')

    while not game.game_over:
        game.hero.update(game)
        game.blitter.blit_all(game.level)
        pygame.display.flip()
        game.fpsClock.tick(con.DISPLAY["FPS"])
        game.get_events()

        if K_ESCAPE in game.events:
            game.game_over = True

    #Save game
    game.game_loader.save_hero(game.hero)
    # game.game_loader.save_levels(game.explored_areas)
    # game.game_loader.save_blit_registry(game.blitter.blit_registry)

    logging.info("Game over! End loop.")
    pygame.quit()
    sys.exit("Goodbye.")

if __name__ == "__main__":
    main()