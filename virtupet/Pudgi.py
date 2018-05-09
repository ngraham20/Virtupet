# This file contains the Pudgi creature and its information

import pygame
import random
import constants
import logger
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
        self.sprite_sheet_s = None

        self.handler = JSONHandler()

        self.personality = None
        self.happiness = None
        self.color = None
        self.parents = [None, None]
        self.vitality = None

        if load_file is not None:  # load should be a filename
            self.import_from_json(load_file)

        else:  # create a new pudgi

            if parents is not None:
                alpha = parents[0]
                beta = parents[1]

                handler = JSONHandler()
                handler.load_file("./data/pudgies/" + alpha + ".json")
                alpha_json = handler.get_data()
                handler.load_file("./data/pudgies/" + beta + ".json")
                beta_json = handler.get_data()

                self.dna = Pudgi.generate_dna_from(alpha_json, beta_json)
                Pudgi.mutate_dna_strand(self.dna.get_strand())
                self.parents = [alpha_json["name"], beta_json["name"]]
            else:
                self.dna = DNA()
                self.dna.gen_rand()

            self.handler.load_file(constants.DEFAULT_PUDGI)
            self.json_object = self.handler.get_data()
            self.happiness = self.json_object["happiness"]
            self.uid = hex(random.randint(0, 100000))
            self.vitality = self.json_object["vitality"]
            self.sleeping = self.json_object["sleeping"]

            self.handler.load_file("./data/names.json")
            names = self.handler.get_data()
            self.name = random.choice(names)

        self.handler.close()

        # ------- general data -------
        self.known_decisions = self.json_object["known_decisions"]
        self.age = self.json_object["age"]
        self.lifespan = random.randint(540, 660)  # approximately 10 minute irl lifespan

        # TODO move this so it only happens upon creation of new Pudgi. Load pudgi should grab json attributes
        self.splice_dna()

        # ------- animation variables -------
        self.change_x = 0
        self.change_y = 0

        self.walking_frames_l = []
        self.walking_frames_r = []
        self.walking_frames_s = []
        # load z's animation
        self.walking_frames_z = []

        self.current_frame = 0
        self.len_animation = None

        self.load_animations()

        self.direction = "R"

        self.image = self.walking_frames_r[self.current_frame]

        self.rect = self.image.get_rect()

        self.level = None

    @staticmethod
    def generate_dna_from(alpha, beta):
        # handler = JSONHandler()
        # handler.load_file("./data/pudgies/" + alpha + ".json")
        # alpha_json = handler.get_data()
        # handler.load_file("./data/pudgies/" + beta + ".json")
        # beta_json = handler.get_data()
        #
        # alpha_dna = DNA(alpha_json["dna"])
        # beta_dna = DNA(beta_json["dna"])

        alpha_dna = DNA(alpha["dna"])
        beta_dna = DNA(beta["dna"])

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
        self.sprite_sheet_s = SpriteSheet(node["S"])

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

        # load sleeping animation
        sprite_count = 0
        for y in range(0, 828):
            if sprite_count == 60:
                break
            for x in range(0, 912):
                if x % 138 == 0 and y % 114 == 0:
                    if sprite_count == 60:
                        break
                    sprite_count += 1
                    image = self.sprite_sheet_s.get_image(x, y, 138, 114)
                    self.walking_frames_s.append(image)

        self.len_animation = sprite_count

    def update(self):
        self.rect.x += self.change_x

        if self.direction == "R":
            self.image = self.walking_frames_r[self.current_frame]
        elif self.direction == "L":
            self.image = self.walking_frames_l[self.current_frame]
        elif self.direction == "S":
            self.image = self.walking_frames_s[self.current_frame]
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

    def import_from_json(self, load):
        self.handler.load_file(load)
        self.json_object = self.handler.get_data()
        self.name = self.json_object["name"]
        self.uid = self.json_object["uid"]
        self.parents = self.json_object["parents"]
        self.personality = self.json_object["personality"]
        self.color = self.json_object["color"]
        self.happiness = self.json_object["happiness"]
        strand = self.json_object["dna"]
        self.dna = DNA(strand)
        self.handler.close()

        logger.logging.info("---Importing Pudgi---")
        logger.logging.info("UID: " + str(self.uid))
        logger.logging.info("Name: " + self.name)
        logger.logging.info("Color: " + self.color)
        logger.logging.info("Personality: " + self.personality)
        logger.logging.info("Parents: " + str(self.parents))

    def export_to_json(self):
        # write information about self to a json file
        self.json_object["name"] = self.name
        self.json_object["uid"] = self.uid
        self.json_object["color"] = self.color
        self.json_object["happiness"] = self.happiness
        self.json_object["personality"] = self.personality
        self.json_object["known_decisions"] = self.known_decisions
        self.json_object["parents"] = self.parents
        self.json_object["dna"] = self.dna.get_strand()

        self.handler.save_as("./data/pudgies/" + self.uid + ".json", self.json_object)

        logger.logging.info("")
        logger.logging.info("---Exporting Pudgi---")
        logger.logging.info("UID: " + str(self.uid))
        logger.logging.info("Name: " + self.name)
        logger.logging.info("Color: " + self.color)
        logger.logging.info("Happiness: " + str(self.happiness))
        logger.logging.info("Personality: " + self.personality)
        logger.logging.info("Parents: " + str(self.parents))
        return

    @staticmethod
    def select_parents(active_agent_list):
        """
        :param active_agent_list:
        :type active_agent_list: list
        :return:
        """

        high_happiness = []
        parents = []
        for pudgi in active_agent_list:
            if pudgi.happiness > 9:
                high_happiness.append(pudgi)
        for i in range(len(high_happiness)):
            if len(high_happiness) >= 2:
                parent01 = high_happiness.pop()
                parent02 = high_happiness.pop()
                parents.append((parent01.uid, parent02.uid))
                parent01.happiness = 2.0
                parent01.vitality -= 4
                parent02.happiness = 2.0
                parent02.vitality -= 4

        return parents

    def make_decision(self):
        self.handler.load_file("./data/decisions.json")
        decision_file = self.handler.get_data()
        self.handler.load_file("./data/pudgies/" + self.uid + ".json")
        choice_index = -1
        happiness_optimized = 0
        t = 0
        choice = None

        w_att = self.weights["attachment"]
        w_hum = self.weights["humor"]
        w_enj = self.weights["enjoyment"]
        w_exc = self.weights["excitement"]
        w_conf = self.weights["confidence"]
        w_cont = self.weights["contentment"]
        w_vit = self.weights["vitality"]
        w_phy = self.weights["physical"]
        w_ment = self.weights["mental"]

        vitality = self.vitality
        chance_waking = -1
        chance_sleeping = -1
        # check vitality for sleepiness (using fuzzy logic)
        low = 2.5
        high = 9
        if vitality <= low:
            chance_waking = 0
            chance_sleeping = 1
        elif low < vitality < high:
            chance_waking = ((vitality-low)/high-low)
            chance_sleeping = ((high - vitality) / high-low)
        else:
            chance_waking = 1
            chance_sleeping = 0

        if self.sleeping:
            if random.random() <= chance_waking:
                self.sleeping = False
        else:
            if random.random() <= chance_sleeping:
                self.sleeping = True  # the pudgi fell asleep

        if not self.sleeping:

            if random.random() > 0.5:
                index = 0
                for decision in self.known_decisions:
                    name = decision["name"]

                    att = None
                    hum = None
                    enj = None
                    exc = None
                    conf = None
                    cont = None
                    vit = None
                    phy = None
                    ment = None
                    ent = None

                    for dec in decision_file:
                        if dec["name"] == name:

                            att = dec["values"]["attachment"]
                            hum = dec["values"]["humor"]
                            enj = dec["values"]["enjoyment"]
                            exc = dec["values"]["excitement"]
                            conf = dec["values"]["confidence"]
                            cont = dec["values"]["contentment"]
                            vit = dec["values"]["vitality"]
                            phy = dec["values"]["physical_energy"]
                            ment = dec["values"]["mental_energy"]
                            ent = dec["values"]["entertainment"]

                    for dec in self.known_decisions:
                        if dec["name"] == name:
                            t = dec["count"]

                    happiness = .5 * (pow(ent, t) + ((pow(att, w_att))+(pow(hum, w_hum))+(pow(enj, w_enj)) +
                                             (pow(exc, w_exc)) + (pow(conf, w_conf))+(pow(cont, w_cont)) -
                                             (pow(vit, w_vit)) - (pow(phy, w_phy)) - (pow(ment, w_ment))))

                    if happiness > happiness_optimized:
                        happiness_optimized = happiness
                        choice = decision
                        choice_index = index

                    self.vitality -= vit
                    index += 1

            else:
                dec_attempt = random.choice(decision_file)
                for known in self.known_decisions:  # iterate through all known
                        if dec_attempt["name"] == known["name"]:  # if we find a match, break out. We don't want this
                            break
                else:
                    choice = dec_attempt
                    att = choice["values"]["attachment"]
                    hum = choice["values"]["humor"]
                    enj = choice["values"]["enjoyment"]
                    exc = choice["values"]["excitement"]
                    conf = choice["values"]["confidence"]
                    cont = choice["values"]["contentment"]
                    vit = choice["values"]["vitality"]
                    phy = choice["values"]["physical_energy"]
                    ment = choice["values"]["mental_energy"]
                    ent = choice["values"]["entertainment"]

                    happiness_optimized = .5 * (pow(ent, t)+((pow(att, w_att)) + (pow(hum, w_hum)) + (pow(enj, w_enj)) +
                                                       (pow(exc, w_exc)) + (pow(conf, w_conf)) + (pow(cont, w_cont)) -
                                                       (pow(vit, w_vit)) - (pow(phy, w_phy)) - (pow(ment, w_ment))))

                    self.known_decisions.append({"name": choice["name"], "count": 0})
                    choice_index = len(self.known_decisions) - 1
                    self.vitality -= vit

            if choice is not None:
                if self.happiness + happiness_optimized <= 0:
                    self.happiness = 0
                else:
                    if self.happiness + happiness_optimized <= 10:
                        self.happiness += happiness_optimized
                    else:
                        self.happiness = 10

                self.known_decisions[choice_index]["count"] += 1

                logger.logging.info("")
                logger.logging.info("---------------------------------------------")
                logger.logging.info("Pudgi: " + self.name)
                logger.logging.info("Choice: " + choice["name"])
                logger.logging.info("Happiness increased by: " + str(happiness_optimized))
                logger.logging.info("Times chosen: " + str(self.known_decisions[choice_index]["count"]))
                logger.logging.info("---------------------------------------------")
                logger.logging.info(str(self.name) + "'s Happiness: " + str(self.happiness))
                logger.logging.info(str(self.name) + "'s Vitality: " + str(self.vitality))

        else:  # the pudgi is sleeping
            self.vitality += 0.8

            logger.logging.info("")
            logger.logging.info("---------------------------------------------")
            logger.logging.info("Pudgi: " + self.name)
            logger.logging.info("Choice: Sleep")
            logger.logging.info("Vitality increased by: 0.8")
            logger.logging.info("---------------------------------------------")
            logger.logging.info(str(self.name) + "'s Happiness: " + str(self.happiness))
            logger.logging.info(str(self.name) + "'s Vitality: " + str(self.vitality))

    def movement(self, direction):
        if direction == "L" and self.rect.x > 0:
            self.go_left()
        elif direction == "R" and self.rect.x < 760:
            self.go_right()
        else:
            self.stop()

