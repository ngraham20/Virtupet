# This file contains the Pudgi creature and its information

import pygame
import random
import constants
from file_handler import JSONHandler
from spritesheet_functions import SpriteSheet
from dna import DNA


class Pudgi(pygame.sprite.Sprite):

    def __init__(self, parents=None, load_file=None):

        super().__init__()

        # self.name = None
        # self.uid = None

        self.weights = {}
        self.sprite_sheet_l = None
        self.sprite_sheet_r = None

        self.handler = JSONHandler()

        self.personality = None
        self.color = None
        self.parents = [None, None]

        if load_file is not None:  # load should be a filename
            self.import_from_json(load_file)

        else:  # create a new pudgi

            self.name = "Pudgi"
            self.uid = hex(random.randint(0, 100000))

            if parents is not None:
                alpha = parents[0]
                beta = parents[1]
                self.dna = Pudgi.generate_dna_from(alpha, beta)
                Pudgi.mutate_dna_strand(self.dna.get_strand())
                self.parents = parents
            else:
                self.dna = DNA()
                self.dna.gen_rand()  # todo modify this for proper randomization of genes

            self.handler.load_file(constants.DEFAULT_PUDGI)
            self.json_object = self.handler.get_data()
            self.json_object["dna"] = self.dna.get_strand()
            self.json_object["uid"] = self.uid
            self.handler.close()

        # ------- general data -------
        self.known_decisions = []
        self.known_decisions = self.json_object["known_decisions"]

        self.splice_dna()

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

    @staticmethod
    def generate_dna_from(alpha, beta):
        handler = JSONHandler()
        handler.load_file("./data/pudgies/" + alpha + ".json")
        alpha_json = handler.get_data()
        handler.load_file("./data/pudgies/" + beta + ".json")
        beta_json = handler.get_data()

        alpha_dna = DNA(alpha_json["dna"])
        beta_dna = DNA(beta_json["dna"])

        strand = DNA.combine_dna(alpha_dna, beta_dna)
        return DNA(strand)

    @staticmethod
    def mutate_dna_strand(strand):
        count = random.randint(1, 5)
        chance = 0.1  # each attempt has a 1/10 chance of mutation
        for num in range(count):
            index = random.randint(0, len(strand) - 1)
            if random.random() <= chance:
                strand[index] = 0 if strand[index] else 1

    def splice_dna(self):
        chromosomes = self.dna.get_chromosomes("behavior")
        self.decode_behavior(chromosomes)

        chromosomes = self.dna.get_chromosomes("color")
        self.decode_color(chromosomes)

        # chromosomes = self.dna.get_chromosomes("personality")
        self.decode_personality()

    def decode_behavior(self, chromosomes):
        for chromosome in chromosomes:
            key = list(chromosome.keys())[0]
            alpha = chromosome[key]["a1"]
            beta = chromosome[key]["a2"]

            if alpha[0] > beta[0]:
                number = alpha[1:]
            elif alpha[0] == beta[0]:
                number = random.choice([alpha, beta])[1:]
            else:
                number = beta[1:]

            bin_num = int(''.join(map(str, number)), base=2) #bin_num is the actual number out of 63
            self.weights[key] = 1 / (bin_num + 1)

    def decode_color(self, chromosomes):
        alpha = chromosomes[0]["color"]["a1"]
        beta = chromosomes[0]["color"]["a2"]
        if alpha[0] > beta[0]:
            number = alpha[1:]
        elif alpha[0] == beta[0]:
            number = random.choice([alpha, beta])[1:]
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

        # set color from dna
        self.color = node["Color"]

    # def decode_personality(self, chromosomes):
    #     alpha = chromosomes[0]["personality"]["a1"]
    #     beta = chromosomes[0]["personality"]["a2"]
    #     if alpha[0] > beta[0]:
    #         number = alpha[1:]
    #     elif alpha[0] == beta[0]:
    #         number = random.choice([alpha, beta])[1:]
    #     else:
    #         number = beta[1:]
    #
    #     self.handler.load_file("./data/personality_metadata.json")
    #     data = self.handler.get_data()
    #     node = data["root"]
    #     for char in number:
    #         node = node[str(char)]
    #
    #     self.personality = node
    def decode_personality(self):
        self.handler.load_file("./data/meyers_metadata.json")
        data = self.handler.get_data()
        attribute = []
        attachment = self.weights["attachment"]
        attachment = int((pow(attachment, -1)) % 16)
        attribute.append(data["attachment"][attachment])

        humor = self.weights["humor"]
        humor = int((pow(humor, -1)) % 16)
        attribute.append(data["humor"][humor])

        enjoyment = self.weights["enjoyment"]
        enjoyment = int((pow(enjoyment, -1)) % 16)
        attribute.append(data["enjoyment"][enjoyment])

        confidence = self.weights["confidence"]
        confidence = int((pow(confidence, -1)) % 16)
        attribute.append(data["confidence"][confidence])

        contentment = self.weights["contentment"]
        contentment = int((pow(contentment, -1)) % 16)
        attribute.append(data["contentment"][contentment])

        vitality = self.weights["vitality"]
        vitality = int((pow(vitality, -1)) % 16)
        attribute.append(data["vitality"][vitality])

        physical = self.weights["physical"]
        physical = int((pow(physical, -1)) % 16)
        attribute.append(data["physical"][physical])

        mental = self.weights["mental"]
        mental = int((pow(mental, -1)) % 16)
        attribute.append(data["mental"][mental])

        #personality = self.weights["personality"]
        #personality = int((pow(personality, -1)) % 16)
        #attribute.append(data["personality"][personality])

        most_common = None
        most = 0
        for item in attribute:
            num = attribute.count(item)
            if num > most:
                most = num
                most_common = item

        self.personality = most_common

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
        self.change_x = 3
        self.direction = "R"

    def go_left(self):
        self.change_x = -3
        self.direction = "L"

    def stop(self):
        self.change_x = 0

    def make_decision(self):
        # make decision
        return

    def import_from_json(self, load):
        self.handler.load_file(load)
        self.json_object = self.handler.get_data()
        self.name = self.json_object["name"]
        self.uid = self.json_object["uid"]
        self.parents = self.json_object["parents"]
        self.personality = self.json_object["personality"]
        self.color = self.json_object["color"]
        strand = self.json_object["dna"]
        self.dna = DNA(strand)
        self.handler.close()

        print("---Importing Pudgi---")
        print("UID: " + str(self.uid))
        print("Name: " + self.name)
        print("Color: " + self.color)
        print("Personality: " + self.personality)
        print("Parents: " + str(self.parents))

    def export_to_json(self):
        # write information about self to a json file
        self.json_object["color"] = self.color
        #self.json_object["personality"] = self.personality
        self.json_object["known_decisions"] = self.known_decisions
        self.json_object["parents"] = self.parents

        self.handler.save_as("./data/pudgies/" + self.uid + ".json", self.json_object)

        print("---Exporting Pudgi---")
        print("UID: " + str(self.uid))
        print("Name: " + self.name)
        print("Color: " + self.color)
        print("Personality: " + str(self.personality))
        print("Parents: " + str(self.parents))
        return
