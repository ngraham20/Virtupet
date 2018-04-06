# This file contains the Pudgi creature and its information

import pygame
import constants
from file_handler import JSONHandler
from spritesheet_functions import SpriteSheet
from dna import DNA


class Pudgi(pygame.sprite.Sprite):

    def __init__(self):

        super().__init__()

        self.name = None

        self.weights = {}

        self.sprite_sheet_l = None
        self.sprite_sheet_r = None

        self.dna = DNA()
        self.dna.gen_rand()  # todo modify this for proper randomization of genes

        self.handler = JSONHandler()
        self.handler.load_file(constants.BLUEPUDGI)
        self.json_object = self.handler.get_data()
        self.json_object["dna"] = self.dna.get_dna_strand()
        self.handler.save(self.json_object)
        self.handler.close()

        self.splice_dna()

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

    def splice_dna(self):
        chromosomes = self.dna.get_chromosomes("behavior")
        self.decode_behavior(chromosomes)

        chromosomes = self.dna.get_chromosomes("color")
        self.decode_color(chromosomes)

        chromosomes = self.dna.get_chromosomes("personality")
        self.decode_personality(chromosomes)

    def decode_behavior(self, chromosomes):
        for chromosome in chromosomes:
            key = list(chromosome.keys())[0]
            alpha = chromosome[key]["a1"]
            beta = chromosome[key]["a2"]

            if alpha[0] >= beta[0]:
                number = alpha[1:]
            else:
                number = beta[1:]

            bin_num = int(''.join(map(str, number)), base=2)
            self.weights[key] = 1 / (bin_num + 1)

    def decode_color(self, chromosomes):
        alpha = chromosomes[0]["color"]["a1"]
        beta = chromosomes[0]["color"]["a2"]
        if alpha[0] >= beta[0]:
            number = alpha[1:]
        else:
            number = beta[1:]

        self.handler.load_file("./data/color_metadata.json")
        data = self.handler.get_data()
        node = data["root"]
        for char in number:
            node = node[str(char)]

        # set sprite sheets from dna
        self.sprite_sheet_l = SpriteSheet(node["L"])
        self.sprite_sheet_r = SpriteSheet(node["R"])

    def decode_personality(self, chromosomes):
        alpha = chromosomes[0]["personality"]["a1"]
        beta = chromosomes[0]["personality"]["a2"]
        if alpha[0] >= beta[0]:
            number = alpha[1:]
        else:
            number = beta[1:]

        self.handler.load_file("./data/personality_metadata.json")
        data = self.handler.get_data()
        node = data["root"]
        for char in number:
            node = node[str(char)]

        print(node)

    def load_animations(self):
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
