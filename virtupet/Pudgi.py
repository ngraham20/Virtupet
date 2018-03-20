# This file contains the Pudgi creature and its information

import pygame
import constants
from spritesheet_functions import SpriteSheet


class Pudgi(pygame.sprite.Sprite):

    def __init__(self):

        super().__init__()

        self.name = None

        # ------- heuristic weights  -------
        self.wattachment = None
        self.whumor = None
        self.wenjoyment = None
        self.wexcitement = None
        self.wconfidence = None
        self.wcontentment = None
        self.wvitality = None
        self.wpenergy = None
        self.wmenergy = None
        self.entertainment = None

        # ------- action variables -------
        self.known_actions = []
        self.new_actions = []

        # ------- animation variables -------
        self.change_x = 0
        self.change_y = 0

        self.walking_frames_l = []
        self.walking_frames_r = []

        self.current_frame = 0
        self.len_animation = None

        self.load_animations()

        self.direction = "R"

        self.image = self.walking_frames_r[self.current_frame]

        self.rect = self.image.get_rect()

        self.level = None

    def load_animations(self):
        sprite_sheet_r = SpriteSheet("./assets/pudgi-blue-r.png")
        sprite_sheet_l = SpriteSheet("./assets/pudgi-blue-l.png")

        # load right animation
        sprite_count = 0
        for y in range(0, 828):
            if sprite_count == 60:
                break
            for x in range(0, 912):
                if x % 138 == 0 and y % 114 == 0:
                    if sprite_count == 60:
                        break
                    sprite_count += 1
                    image = sprite_sheet_r.get_image(x, y, 138, 114)
                    self.walking_frames_r.append(image)

        self.len_animation = sprite_count

        # load left animation
        sprite_count = 0
        for y in range(0, 828):
            if sprite_count == 60:
                break
            for x in range(0, 912):
                if x % 138 == 0 and y % 114 == 0:
                    if sprite_count == 60:
                        break
                    sprite_count += 1
                    image = sprite_sheet_l.get_image(x, y, 138, 114)
                    self.walking_frames_l.append(image)

        self.len_animation = sprite_count

    def update(self):
        self.rect.x += self.change_x

        if self.direction == "R":
            self.image = self.walking_frames_r[self.current_frame]
        else:
            self.image = self.walking_frames_l[self.current_frame]
        self.current_frame += 1

        if self.current_frame >= self.len_animation:
            self.current_frame = 0

    def go_right(self):
        self.change_x = 6
        self.direction = "R"

    def go_left(self):
        self.change_x = -6
        self.direction = "L"

    def stop(self):
        self.change_x = 0

    def make_decision(self):
        # make decision
        return

    def export(self):
        # write information about self to a json file
        return

