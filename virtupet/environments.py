import pygame
import constants
from file_handler import JSONHandler


class Environment:

    def __init__(self, agent):

        handler = JSONHandler()
        handler.load_file('./data/environments.json')
        self.json_object = handler.get_data()

        self.background = None
        self.enemy_list = None
        self.agent = agent

        self.enemy_list = pygame.sprite.Group()

    def update(self):
        self.enemy_list.update()

    def draw(self, screen):
        screen.fill(constants.BLUE)
        screen.blit(self.background, (0, 0))

        self.enemy_list.draw(screen)


class EnvironmentHouse(Environment):

    def __init__(self, agent):

        Environment.__init__(self, agent)

        # todo make background 300x200
        self.background = pygame.image.load(self.json_object["dither"]["background"]).convert()
        self.background.set_colorkey(constants.WHITE)
