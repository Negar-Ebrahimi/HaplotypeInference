import math
import numpy


def resolutions_size(genotype):
    number_of_recessive_alleles = 0
    for allele in genotype:
        if allele == 2:
            number_of_recessive_alleles += 1
    # The number of resolutions will be half of the all possible parents ('cause they're coupled)
    if number_of_recessive_alleles == 0:
        return 0
    return 2**(number_of_recessive_alleles - 1)


def expand_resolution(genotype, resolution_number):
    if resolution_number > resolutions_size(genotype):  # Is this resolution_number available in the genotype
        return False
    haplotype_mother = ()
    haplotype_father = ()
    recessive_alleles = ''
    if resolutions_size(genotype) > 0:
        recessive_alleles = ("{0:b}".format(resolution_number)).zfill(int(math.log(resolutions_size(genotype), 2)) + 1)
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


def initial_scoring(genotypes):
    for genotype_index in range(len(genotypes)):
        number_of_resolutions = resolutions_size(genotypes[genotype_index])
        resolutions_scores = []
        for resolution_number in range(number_of_resolutions):
            resolutions_scores.append(1 / number_of_resolutions)
        scores.append(resolutions_scores)
    return scores


def score_the_path(path, total_score):
    # todo: This formula should be optimized: use max-min ant system method (binary?)
    splitted_score = total_score / len(path)
    for genotype_index in range(len(path)):
        resolution_number = path[genotype_index]
        scores[genotype_index][resolution_number] += splitted_score
    proportionate_resolutions_scores()
    return scores


def proportionate_resolutions_scores():
    # reduce sum of the scores to 1 while keeping the same proportional of a genotype resolutions scores
    for genotype_index in range(len(genotypes)):
        genotype = genotypes[genotype_index]
        sum_of_genotype_resolutions_scores = numpy.sum(scores[genotype_index])
        for resolution_number in range(resolutions_size(genotype)):
            scores[genotype_index][resolution_number] =\
                scores[genotype_index][resolution_number] / sum_of_genotype_resolutions_scores
    return scores


def assign_agent():
    path_resolutions_numbers = []
    haplotypes = ()
    for genotype_index in range(len(genotypes)):
        genotype = genotypes[genotype_index]
        if resolutions_size(genotype) > 0:
            path_resolutions_numbers.append(
                numpy.random.choice(range(resolutions_size(genotype)), p=scores[genotype_index]),)
        else:
            path_resolutions_numbers.append(0)
        haplotypes = haplotypes + (expand_resolution(genotype, path_resolutions_numbers[-1])[0],) # Add mother
        haplotypes = haplotypes + (expand_resolution(genotype, path_resolutions_numbers[-1])[1],) # Add father

    total_score = 2*len(genotypes) - len(set(haplotypes))
    score_the_path(path_resolutions_numbers, total_score)
    return total_score


answers = []
for l in range(100):
    # extracting the input data
    with open("SmallSampleInput.txt") as file:
        n, m = [int(x) for x in next(file).split()]
        genotypes = []
        for line in file:  # read rest of lines
            genotypes.append([int(x) for x in line.split()])

        scores = []
        initial_scoring(genotypes)

        # for 40 ants
        arr = []
        for i in range(50):
            arr.append(2*len(genotypes) - assign_agent())
        answers.append(min(arr))
print(answers)
