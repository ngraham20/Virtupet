# This file contains the Pudgi creature and its information

import pygame
import random
import constants
from file_handler import JSONHandler
from spritesheet_functions import SpriteSheet
from dna import DNA


class Pudgi(pygame.sprite.Sprite):

    def __init__(self):

        super().__init__()

        self.name = None

        # ------- heuristic -------
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

        # ------- heuristic weights  -------

        # randomize weights out of 1 and 10 todo move the randomizer to randomize the dna
        # def randomize():
        #     range(1)
        #     return random.randint(1, 11)
        # self.wattachment = randomize()
        # self.whumor = randomize()
        # self.wenjoyment = randomize()
        # self.wexcitement = randomize()
        # self.wconfidence = randomize()
        # self.wcontentment = randomize()
        # self.wvitality = randomize()
        # self.wpenergy = randomize()
        # self.wmenergy = randomize()
        # self.entertainment = randomize()

        self.handler = JSONHandler()
        self.handler.load_file(constants.BLUEPUDGI)
        self.json_object = self.handler.get_data()

        self.dna = DNA()
        self.dna.gen_rand()  # todo modify this for proper randomization of genes
        self.json_object["dna"] = self.dna.get_dna_strand()
        self.handler.save(self.json_object)



        # ------- action variables -------
        self.known_actions = []
        self.new_actions = []

        # ------- animation variables -------
        self.change_x = 0
        self.change_y = 0

        self.sprite_sheet_l = None
        self.sprite_sheet_r = None

        self.walking_frames_l = []
        self.walking_frames_r = []

        self.current_frame = 0
        self.len_animation = None

        self.load_animations()

        self.direction = "R"

        self.image = self.walking_frames_r[self.current_frame]

        self.rect = self.image.get_rect()

        self.level = None

    def decode_dna(self):

        # -------------- set up chromosomes -------------
        b_chroms = self.dna.get_chromosome_values("behavior")
        c_chroms = self.dna.get_chromosome_values("color")
        p_chroms = self.dna.get_chromosome_values("personality")

        # ---------------- color chromosomes --------------
        c_alpha = c_chroms[0]["a1"]
        c_beta = c_chroms[1]["a2"]
        if c_alpha[0] >= c_beta[0]:
            number = c_alpha[1:]
        else:
            number = c_beta[1:]

        number = [0, 1, 1]  # todo once the other colors are in place, remove this to allow the system to derive color
        self.handler.load_file("./data/metadata.json")
        data = self.handler.get_data()
        node = data["root"]
        for char in number:
            node = node[str(char)]

        # set sprite sheets from dna
        self.sprite_sheet_l = SpriteSheet(node["L"])
        self.sprite_sheet_r = SpriteSheet(node["R"])

        # todo use dna to get other information too

        # ----------------- behavior chromosomes -----------

        # ----------------- personality chromosomes --------------

    def load_animations(self):
        self.decode_dna()

        # self.sprite_sheet_r = SpriteSheet(self.json_object["animations"]["R"])
        # self.sprite_sheet_l = SpriteSheet(self.json_object["animations"]["L"])
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
                    image = self.sprite_sheet_r.get_image(x, y, 138, 114)
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
                    image = self.sprite_sheet_l.get_image(x, y, 138, 114)
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
