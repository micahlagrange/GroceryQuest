__author__ = "micah turner"

import os
import logging

PREFERENCES = {
    'KEY_REPEAT_ON': True,
    'KEY_DELAY': 50,
    'KEY_REPEAT': 20,
    'MENU_FONT_SIZE': 25,
    'MENU_FONT': 'resources/fonts/freesansbold.ttf',
    'HERO_NAME': 'Hero_name',
    'LOG_LEVEL': 'DEBUG'
}

PROFILE_NAME = PREFERENCES['HERO_NAME']

PATHS = {
    'sprites': os.path.join("resources", "sprites"),
    'entities': os.path.join("resources", "entities"),
    'backgrounds': os.path.join("resources", "backgrounds"),
    'sounds': os.path.join("resources", "sounds"),
    'maps': os.path.join("resources", "maps"),
    'logs': os.path.join("data", "logs"),
    'save_dir': os.path.join("data", PROFILE_NAME),
}

for key, path in PATHS.items():
    if not os.path.exists(path):
        logging.debug('Could not find {} directory in the project path'.format(path))
        os.makedirs(path)
        logging.debug('Created path ' + path)


GAME_CONSTANTS = {
    'GAME_TITLE': 'Grocery Quest',
    'TILE': 20,
    'LIVES': 3,
    'KILL_ALL': 0,
    'MAP_TOP_LEFT': (20, 60),
    'MAP_LEFT_EDGE': 19,
    'MAP_RIGHT_EDGE': 619,
    'MAP_TOP_EDGE': 59,
    'MAP_BOTTOM_EDGE': 479
}


DIFFICULTY = {
    'AGGRO_DIST': 5,
    'HERO_SPEED': 20,
    'ENEMY_SPEED': 10,
    'INVENTORY_SIZE': 20
}

DISPLAY = {
    'RESOLUTION': (640, 480),
    'VIEWFRAME_OFFSET': (20, 60),
    'FPS': 30,
    'FULLSCREEN': 0,
}

COLORS = {
    'RED': (255, 0, 0), 'FUCHSIA': (255, 0, 255), 'PURPLE': (128, 0, 128), 'MAROON': (128, 0, 0),
    'GREEN': (0, 128, 0), 'OLIVE': (128, 128, 0), 'LIME': (0, 255, 0), 'BLUE': (0, 0, 255),
    'NAVY_BLUE': (0, 0, 128), 'TEAL': (0, 128, 128), 'AQUA': (0, 255, 255), 'YELLOW': (255, 255, 0),
    'BLACK': (0, 0, 0), 'GRAY': (128, 128, 128), 'SILVER': (192, 192, 192), 'WHITE': (255, 255, 255),
}

SOUND_SETTINGS = {
    'num_channels': 16,
    'reserved_channels': 8,
    'bgm_volume': .5,
    'sfx_volume': .5,
    'stereo_channels': 2,
    'bgm_fade_in': 100,
}

logging.basicConfig(
    filename=os.path.join(PATHS['logs'], 'gc.log'),
    level=PREFERENCES['LOG_LEVEL'],
    datefmt='%m-%d %H:%M',
    format='%(asctime)s :%(levelname)s:%(name)s: %(message)s')
logging.debug('logging enabled at path: ' + PATHS['logs'])
