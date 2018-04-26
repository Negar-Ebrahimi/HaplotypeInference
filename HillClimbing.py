def calculate_heuristic(genotypes):
    heuristic = []
    for genotype in genotypes:
        non_compatibles = set()
        for index in range(len(genotype)):
            allele = genotype[index]
            if allele != 2:
                for anotherGenotype in genotypes:
                    # for each allele of the main genotype, every n-1 others are checked for  compatibility
                    if anotherGenotype[index] != allele and anotherGenotype[index] != 2:
                        non_compatibles.add(
                            genotypes.index(anotherGenotype))  # this genotype is added to non compatible set
                heuristic.append(len(non_compatibles))

    return heuristic


def initial_state(genotypes):
    w, h = len(genotypes[0]), 2*len(genotypes)
    haplotypes = [[0 for x in range(w)] for y in range(h)]
    for genotype_index in range(len(genotypes)):
        genotype = genotypes[genotype_index]
        for allele_index in range(len(genotype)):
            allele = genotype[allele_index]
            if allele != 2:  # It's a dominant allele.
                haplotypes[2*genotype_index][allele_index] = allele
                haplotypes[2*genotype_index + 1][allele_index] = allele
            else:   # It's a recessive allele.
                haplotypes[2 * genotype_index][allele_index] = 0
                haplotypes[2 * genotype_index + 1][allele_index] = 1

    return haplotypes


with open("SampleInput.txt") as file:
    n, m = [int(x) for x in next(file).split()]
    genotypes = []
    for line in file:  # read rest of lines
        genotypes.append([int(x) for x in line.split()])


print(n, m, genotypes, "************")

heuristic = calculate_heuristic(genotypes)

haplotypes = initial_state(genotypes)

print(haplotypes)
