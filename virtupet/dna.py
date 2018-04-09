# this file will handel all dna jobs in the project
import random


class Sequencer:

    def __init__(self):
        self.b_chrom_size = 7
        self.b_genome_count = 9
        self.b_chrom_count = self.b_genome_count * 2

        self.c_chrom_size = 4
        self.c_genome_count = 1
        self.c_chrom_count = self.c_genome_count * 2

        self.p_chrom_size = 5
        self.p_genome_count = 1
        self.p_chrom_count = self.p_genome_count * 2

        self.genome_count = self.b_genome_count
        self.genome_count += self.p_genome_count
        self.genome_count += self.c_genome_count

        self.gene_count = self.b_chrom_size*self.b_chrom_count
        self.gene_count += self.c_chrom_size*self.c_chrom_count
        self.gene_count += self.p_chrom_size*self.p_chrom_count

    # sequence should return a dictionary of genes which represent the heads of the chromosomes
    def sequence(self):

        # list of dict of string -> dict of string -> int
        strand = [{"attachment": {"a1": 0, "a2": 0}},
                  {"humor": {"a1": 0, "a2": 0}},
                  {"enjoyment": {"a1": 0, "a2": 0}},
                  {"excitement": {"a1": 0, "a2": 0}},
                  {"confidence": {"a1": 0, "a2": 0}},
                  {"contentment": {"a1": 0, "a2": 0}},
                  {"vitality": {"a1": 0, "a2": 0}},
                  {"physical": {"a1": 0, "a2": 0}},
                  {"mental": {"a1": 0, "a2": 0}},
                  {"personality": {"a1": 0, "a2": 0}},
                  {"color": {"a1": 0, "a2": 0}
                   }]
        index = 0
        for k in range(self.b_genome_count):
            key = list(strand[k].keys())[0]
            strand[k][key]["a1"] = self.b_chrom_size * k * 2
            strand[k][key]["a2"] = self.b_chrom_size * (2 * k + 1)
            index += 1

        p_begining = self.b_chrom_size * self.b_chrom_count
        key = list(strand[self.b_genome_count:self.b_genome_count + 1][0].keys())[0]
        strand[index][key]["a1"] = p_begining
        strand[index][key]["a2"] = p_begining + self.p_chrom_size
        index += 1

        c_begining = p_begining + self.p_chrom_size * self.p_chrom_count
        key = list(strand[self.b_genome_count + self.p_genome_count:][0].keys())[0]
        strand[index][key]["a1"] = c_begining
        strand[index][key]["a2"] = c_begining + self.c_chrom_size

        return strand


class DNA:

    def __init__(self, dna=None):

        self.sequencer = Sequencer()
        if dna is not None:
            self.dna = dna
        else:
            self.dna = []
        self.indices = self.sequencer.sequence()

    def gen_rand(self):
        # for now, going to fill all with truly random values todo randomize these values within personality bounds
        for index in range(self.sequencer.gene_count):
            self.dna.append(random.randint(0, 1))
        return self.dna

    def get_chromosomes(self, c_type):
        chromosomes = list(dict())
        if c_type == "behavior":
            
            index_count = self.sequencer.b_chrom_size
            genome_count = self.sequencer.b_genome_count
            genome_loc = 0
        elif c_type == "personality":
            index_count = self.sequencer.p_chrom_size
            genome_count = self.sequencer.p_genome_count
            genome_loc = self.sequencer.b_genome_count
        elif c_type == "color":
            index_count = self.sequencer.c_chrom_size
            genome_count = self.sequencer.c_genome_count
            genome_loc = self.sequencer.b_genome_count + self.sequencer.p_genome_count
        else:
            index_count = -1
            genome_loc = -1
            genome_count = -1
            
        for k in range(genome_loc, genome_loc + genome_count):
            key = list(self.indices[k].keys())[0]
            a1 = list(self.indices[k].values())[0]["a1"]
            a2 = list(self.indices[k].values())[0]["a2"]

            c_a1 = list()
            for gene in range(index_count):
                if a1 is not None:
                    c_a1.append(self.dna[a1 + gene])

            c_a2 = list()
            for gene in range(index_count):
                if a2 is not None:
                    c_a2.append(self.dna[a2 + gene])
            chromosomes.append({key: {"a1": c_a1, "a2": c_a2}})

        return chromosomes

    @staticmethod
    def combine_dna(p1, p2):
        """

        :param p1:
        :type p1: DNA
        :param p2:
        :type p2: DNA
        """

        p1_chromosomes = p1.get_chromosomes("behavior")
        p1_chromosomes += p1.get_chromosomes("personality")
        p1_chromosomes += p1.get_chromosomes("color")
        p2_chromosomes = p2.get_chromosomes("behavior")
        p2_chromosomes += p2.get_chromosomes("personality")
        p2_chromosomes += p2.get_chromosomes("color")

        child_chrom_alpha = list()
        child_chrom_beta = list()

        for chromosome in p1_chromosomes:
            key = list(chromosome.keys())[0]
            genome = list()
            genome.append(chromosome[key]["a1"])
            genome.append(chromosome[key]["a2"])
            child_chrom_alpha.append(random.choice(genome))

        for chromosome in p2_chromosomes:
            key = list(chromosome.keys())[0]
            genome = list()
            genome.append(chromosome[key]["a1"])
            genome.append(chromosome[key]["a2"])
            child_chrom_beta.append(random.choice(genome))

        child_chromosomes = [list()]*(len(child_chrom_alpha) + len(child_chrom_beta))
        child_chromosomes[::2] = child_chrom_alpha
        child_chromosomes[1::2] = child_chrom_beta

        return (lambda chroms: [gene for chrom in chroms for gene in chrom])(child_chromosomes)

    def get_strand(self):
        return self.dna

    def set_strand(self, strand):
        self.dna = strand

