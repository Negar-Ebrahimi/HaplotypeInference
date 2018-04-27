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


def initial_state(genotypes):
    haplotypes = []
    for genotype_index in range(len(genotypes)):
        haplotype_father = ()
        haplotype_mother = ()
        genotype = genotypes[genotype_index]
        for allele_index in range(len(genotype)):
            allele = genotype[allele_index]
            if allele != 2:  # It's a dominant allele.
                haplotype_father = haplotype_father + (allele,)
                haplotype_mother = haplotype_mother + (allele,)
            else:   # It's a recessive allele.
                haplotype_father = haplotype_father + (0,)
                haplotype_mother = haplotype_mother + (1,)
        haplotypes.append(haplotype_father)
        haplotypes.append(haplotype_mother)

    return haplotypes


def number_of_diverse_haplotypes(haplotypes):
    return len(set(haplotypes))


def dominant_alleles(genotype):  # returns a list of indices of dominant alleles (value 2) of a genotype
    dominant_alleles_indices = []
    for allele_index in range(len(genotype)):
        if genotype[allele_index] == 2:
            dominant_alleles_indices.append(allele_index)
    return dominant_alleles_indices


def toggle(haplotypes, genotype_index):
    genotype = genotypes[genotype_index]

    haplotype_father = haplotypes[2*genotype_index]
    haplotype_mother = haplotypes[2*genotype_index + 1]

    random_dominant_allele_index = random.choice(dominant_alleles(genotype))

    updated_haplotype_father = ()
    for allele_index in range(len(haplotype_father)):
        allele = haplotype_father[allele_index]
        if allele_index != random_dominant_allele_index:
            updated_haplotype_father = updated_haplotype_father + (allele,)
        else:
            updated_haplotype_father = updated_haplotype_father + (1,)

    updated_haplotype_mother = ()
    for allele_index in range(len(haplotype_mother)):
        allele = haplotype_mother[allele_index]
        if allele_index != random_dominant_allele_index:
            updated_haplotype_mother = updated_haplotype_mother + (allele,)
        else:
            updated_haplotype_mother = updated_haplotype_mother + (0,)
    # toggling is static (father -> 1 & mother -> 0) because we know how we have been assigning in initial state.

    haplotypes.remove(haplotype_father)
    haplotypes.insert(2*genotype_index, updated_haplotype_father)
    # replace the toggled haplotype father tuple in the list

    haplotypes.remove(haplotype_mother)
    haplotypes.insert(2*genotype_index + 1, updated_haplotype_mother)
    # replace the toggled haplotype mother tuple in the list

    return haplotypes

# extracting the input data
with open("SampleInput.txt") as file:
    n, m = [int(x) for x in next(file).split()]
    genotypes = []
    for line in file:  # read rest of lines
        genotypes.append([int(x) for x in line.split()])

heuristics = calculate_heuristic(genotypes)
haplotypes = initial_state(genotypes)

# the hill climbing loop
for heuristic in heuristics:
    if number_of_diverse_haplotypes(toggle(haplotypes, heuristic[0])) >= number_of_diverse_haplotypes(haplotypes):
        # it means this is a flat area and we should stop climbing the hill!
        print('The optimal number of this haplotype inference base on parsimony using hill climbing method is: ',
              number_of_diverse_haplotypes(haplotypes))
        break
    haplotypes = toggle(haplotypes, heuristic[0])
