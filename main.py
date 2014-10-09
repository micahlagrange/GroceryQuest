

__author__ = "micah turner"

import pygame
from pygame.locals import *

import sys
import logging
import pickle
import os

import constants as con
import display
import characters
import levels
import sound


def load_game(save_filename):
    if not os.path.exists(os.path.join(con.PATHS['save_dir'], save_filename)):
        game = Game(levelname="Start", save_filename=save_filename)

    else:
        with open(os.path.join(con.PATHS['save_dir'], save_filename), 'rb') as savefile:
            game = pickle.load(savefile)

    return game


class Game(object):
    def __init__(self, levelname, save_filename, hero_name=con.PREFERENCES["HERO_NAME"]):
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

        self.explored_areas = []
        self.current_bgm = ''

        self.hero = characters.Hero(con.PATHS['save_dir'], save_filename,
                                    name=hero_name, game=self, pos=(0, 0))

        self.level = levels.choose_level(levelname, self)

        self.hero.pos = self.level.startpos

    def __getstate__(self):
        state = self.__dict__.copy()
        del state['soundplayer']
        del state['fpsClock']
        del state['screen']
        del state['blitter']

        state['blit_registry'] = self.blitter.blit_registry
        for key, value in state.items():
            print(str(key) + ':\n')
            print(value)

        return state

    def __setstate__(self, state):
        state['fpsClock'] = pygame.time.Clock()
        state['screen'] = display.ScreenInit()
        state['blitter'] = display.BlitManager(state['screen'])
        self.__dict__.update(state)
        self.blitter.blit_registry = state['blit_registry']


def main():
    game = load_game('save')

    while game.hero.isalive:
        game.hero.update(game)
        game.blitter.blit_all(game.level)
        pygame.display.flip()
        game.fpsClock.tick(con.DISPLAY["FPS"])

if __name__ == "__main__":
    main()