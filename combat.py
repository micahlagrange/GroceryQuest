__author__ = "multivoxmuse"


class Battle(object):
    @staticmethod
    def fight(monster, hero):
        if hero.isalive and monster.isalive:
            return monster.die()