import random

def calculate_heuristic(genotypes):
    heuristic = []
    for genotype_index in range(len(genotypes)):
        genotype = genotypes[genotype_index]
        non_compatibles = set()
        for allele_index in range(len(genotype)):
            allele = genotype[allele_index]
            if allele != 2:
                for anotherGenotype in genotypes:
                    # for each allele of the main genotype, every n-1 others are checked for  compatibility
                    if anotherGenotype[allele_index] != allele and anotherGenotype[allele_index] != 2:
                        non_compatibles.add(
                            genotypes.index(anotherGenotype))  # this genotype is added to non compatible set
        heuristic.append((genotype_index, len(non_compatibles)))
        # appends it as a tuple of (genotype_index, genotype.number_of_non_compatibles)

    return sorted(heuristic, key=lambda tup: tup[1])
    # returns the tuples list sorted by the heuristic value rather than the genotype index

# each node of the search tree is a genotype with an identical heuristic but different f values
def calculate_f(genotype_index, g):
    for heuristic in heuristics:
        if heuristic[0] == genotype_index:
            return g + heuristic[1] # = g(n) + h(n)


def explore(genotype, haplotypes):
    haplotype_father = []
    haplotype_mother = []
    for allele in genotype:
        if allele != 2:
            haplotype_father.append(allele)
            haplotype_mother.append(allele)
        else:
            random_allele_of_father = random.randint(0, 2)
            haplotype_father.append(random_allele_of_father)
            haplotype_mother.append(1 - random_allele_of_father)

    haplotypes.add(haplotype_father)
    haplotypes.add(haplotype_mother)
    return haplotypes

# extracting the input data
with open("SampleInput.txt") as file:
    n, m = [int(x) for x in next(file).split()]
    genotypes = []
    for line in file:  # read rest of lines
        genotypes.append([int(x) for x in line.split()])

heuristics = calculate_heuristic(genotypes)

open_list = []
closed_list = []
