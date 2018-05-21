from random import randint
import math

def resolutions_size(genotype):
    number_of_recessive_alleles = 0
    for allele in genotype:
        if allele == 2:
            number_of_recessive_alleles += 1
    # The number of resolutions will be half of the all possible parents ('cause they're coupled)
    if number_of_recessive_alleles == 0:
        return 1
    return 2**(number_of_recessive_alleles - 1)


def expand_resolution(genotype, resolution_number):
    if resolution_number >= resolutions_size(genotype):  # Is this resolution_number available in the genotype
        return False
    haplotype_mother = ()
    haplotype_father = ()
    recessive_alleles = "{0:b}".format(resolution_number) + "0"
    print('resolution number:', resolution_number)
    print('resolution size:', resolutions_size(genotype))
    print(("{0:b}".format(resolution_number)).zfill(int(math.log(resolutions_size(genotype), 2)) + 1))
    recessive_allele_index = 0
    # Makes the j-th resolution couple of the genotype in which j = resolution_number
    for allele_index in range(len(genotype)):
        allele = genotype[allele_index]
        if allele != 2:  # It's a dominant allele
            haplotype_mother = haplotype_mother + (allele,)
            haplotype_father = haplotype_father + (allele,)
        else:  # It's a recessive allele
            haplotype_mother = haplotype_mother + (int(recessive_alleles[recessive_allele_index]),)
            haplotype_father = haplotype_father + (1 - int(recessive_alleles[recessive_allele_index]),)
            recessive_allele_index += 1
    return [haplotype_mother, haplotype_father]

def fitness(individual):
    haplotypes = ()
    for genotype_index in range(len(genotypes)):
        haplotypes = haplotypes + (expand_resolution(genotypes[genotype_index], individual[genotype_index]),)
    print(haplotypes)
    print(len(set(haplotypes)))
    return len(genotypes) - len(set(haplotypes))

def initial_population(genotypes):
    initial_population = []
    initial_population_size = 2
    for index in range(initial_population_size):
        individual = ()
        for genotype in genotypes:
            individual = individual + (randint(0, resolutions_size(genotype) - 1),)
        initial_population.append(individual)
    return initial_population


# extracting the input data
with open("SmallSampleInput.txt") as file:
    n, m = [int(x) for x in next(file).split()]
    genotypes = []
    for line in file:  # read rest of lines
        genotypes.append([int(x) for x in line.split()])

    print(initial_population(genotypes))
    print(fitness(initial_population(genotypes)[0]))
