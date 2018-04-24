with open("SampleInput.txt") as file:
    n, m = [int(x) for x in next(file).split()]
    genotypes = []
    for line in file: # read rest of lines
        genotypes.append([int(x) for x in line.split()])


print(n, m, genotypes)

h = []
for genotype in genotypes:
    nonCompatibles = set()
    for index in range(len(genotype)):
        allele = genotype[index]
        if allele != 2:
            for anotherGenotype in genotypes:
                # for each allele of the main genotype, every n-1 others are checked for  compatibility
                if anotherGenotype[index] != allele and anotherGenotype[index] != 2:
                    nonCompatibles.add(genotypes.index(anotherGenotype)) # this genotype is added to non compatible set
    h.append(len(nonCompatibles))

print(h)