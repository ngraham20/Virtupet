import pygame
import constants


class Environment:

    def __init__(self, player):

        self.background = None
        self.enemy_list = None
        self.player = player

        self.enemy_list = pygame.sprite.Group()

    def update(self):
        self.enemy_list.update()

    def draw(self, screen):
        screen.fill(constants.BLUE)
        screen.blit(self.background, (0, 0))

        self.enemy_list.draw(screen)


class EnvironmentHouse(Environment):

    def __init__(self, player):

        Environment.__init__(self, player)

        self.background = pygame.image.load("./assets/background_01.png").convert()
        self.background.set_colorkey(constants.WHITE)
