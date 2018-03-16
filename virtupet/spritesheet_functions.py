import pygame
import constants


class SpriteSheet(object):
    def __init__(self, file_name):

        # load the sprite sheet
        self.sprite_sheet = pygame.image.load(file_name).convert()

    def get_image(self, x, y, width, height):
        """ Get a single frame from a sprite sheet
            by passing in its x,y coordinates, along
            with its width and height """

        image = pygame.Surface([width, height]).convert()

        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))

        # Assuming black works as the transparent color
        image.set_colorkey(constants.TRANS)

        return image
