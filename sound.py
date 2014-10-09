__author__ = 'micah'
import os

import pygame

import constants as con


class SoundPlayer():
    def __init__(self):
        self.mixer = self.init_mixer()
        self.sounds_dir = con.PATHS["sounds"]
        self.ambient_channel = self.init_channel(1)
        self.sfx_channel = self.init_channel(9)

    @staticmethod
    def init_mixer():
        mixer = pygame.mixer
        mixer.set_num_channels(con.SOUND_SETTINGS['num_channels'])
        mixer.set_reserved(con.SOUND_SETTINGS['reserved_channels'])
        mixer.init(channels=con.SOUND_SETTINGS['stereo_channels'])

        return mixer

    def init_channel(self, channel_id):
        """Initialize a channel by id (int)"""
        return self.mixer.Channel(channel_id)

    def play_sfx(self, sound_file, loops=0, maxtime=0, fade_ms=0, volume=con.SOUND_SETTINGS['sfx_volume']):
        """
        The simplest way to just play any sound once by file name.
        But you can also set any other sound attribute through arguments.
        """
        sound = self.mixer.Sound(os.path.join(self.sounds_dir, sound_file))
        self.sfx_channel.set_volume(volume)
        self.sfx_channel.play(sound, loops, maxtime, fade_ms)

    def queue_sfx(self, sound_file):
        """Queue any sound by filename"""
        sound = self.mixer.Sound(os.path.join(self.sounds_dir, sound_file))
        self.sfx_channel.queue(sound)

    def play_bgm(self, sound_file, volume=con.SOUND_SETTINGS['bgm_volume'], bgm_fade_in=con.SOUND_SETTINGS['bgm_fade_in']):
        sound = self.mixer.Sound(os.path.join(self.sounds_dir, sound_file))
        self.ambient_channel.set_volume(volume)
        self.ambient_channel.play(sound, loops=-1, fade_ms=bgm_fade_in)

    def set_bgm_volume(self, volume):
        """Set the ambient channel volume"""
        self.ambient_channel.set_volume(volume)

    def set_sfx_volume(self, volume):
        """Set the sfx channel volume"""
        self.sfx_channel.set_volume(volume)