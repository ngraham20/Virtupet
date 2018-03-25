# this file will handel all dna jobs in the project
import random


class Sequencer:

    def __init__(self):
        self.gene_count = 70
        self.b_chrom_size = 6
        self.b_chrom_count = 9
        self.c_chrom_size = 4
        self.c_chrom_count = 2
        self.p_chrom_size = 4
        self.p_chrom_count = 2

    # sequence should return a dictionary of genes which represent the heads of the chromosomes
    def sequence(self):
        genome = {"behavior": [{"attachment": None}, {"humor": None}, {"enjoyment": None},
                               {"excitement": None}, {"confidence": None}, {"contentment": None},
                               {"vitality": None}, {"physical": None}, {"mental": None}],
                  "personality": [{"a1": None}, {"a2": None}],
                  "color": [{"a1": None}, {"a2": None}]}

        for k in range(self.b_chrom_count):  # set behavior chromosome locations
            key = list(genome["behavior"][k].keys())
            genome["behavior"][k][key[0]] = self.b_chrom_size*k

        b_chrom = self.b_chrom_size * self.b_chrom_count
        p_chrom = self.p_chrom_size * self.p_chrom_count

        for k in range(self.p_chrom_count):
            key = list(genome["personality"][k].keys())
            genome["personality"][k][key[0]] = b_chrom + self.p_chrom_size*k

        for k in range(self.c_chrom_count):
            key = list(genome["color"][k].keys())
            genome["color"][k][key[0]] = b_chrom + p_chrom + self.c_chrom_size * k

        return genome


class DNA:

    def __init__(self):

        self.sequencer = Sequencer()
        self.dna = []
        self.indices = self.sequencer.sequence()

    def gen_rand(self):
        # for now, going to fill all with truly random values todo randomize these values within personality bounds
        for index in range(self.sequencer.gene_count):
            self.dna.append(random.randint(0, 1))
        return self.dna

    def get_chromosome_values(self, c_type):
        chromosomes = list(list())
        chromosome = list()
        for k in range(len(self.indices[c_type])):
            index = list(self.indices[c_type][k].values())
            if c_type == "behavior":
                count = self.sequencer.b_chrom_size
            elif c_type == "color":
                count = self.sequencer.c_chrom_size
            elif c_type == "personality":
                count = self.sequencer.p_chrom_size
            else:
                count = -1
            for gene in range(count):
                if index is not None:
                    chromosome.append(self.dna[index[0] + gene])
            chromosomes.append(chromosome)

        return chromosomes
