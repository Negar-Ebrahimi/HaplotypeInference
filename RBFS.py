import math


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


def expand_successors(path):
    successor_genotype_index = current_node['genotype-index'] + 1
    being_expanded_genotype = genotypes[successor_genotype_index]

    min_successor_index = 0
    print(successor_genotype_index)
    for successor_index in range(resolutions_size(being_expanded_genotype)):
        # reset current haplotypes
        current_haplotypes = path

        print('resolution number ', successor_index)
        print((expand_resolution(being_expanded_genotype, successor_index)))
        # temporary addition of the mother haplotype of this resolution to the path
        current_haplotypes = current_haplotypes + (expand_resolution(being_expanded_genotype, successor_index)[0],)

        # temporary addition of the father haplotype of this resolution to the path
        current_haplotypes = current_haplotypes + (expand_resolution(being_expanded_genotype, successor_index)[1],)

        # check for improvement of f-cost
        successor_g_cost = successor_genotype_index + 1
        successor_heuristic_value = len(set(current_haplotypes)) - len(set(path))
        successor_f_cost = successor_g_cost + successor_heuristic_value
        print('f-cost: ', len(set(current_haplotypes)))
        if successor_f_cost <= current_node['f-cost']:
            current_node['genotype-index'] = successor_genotype_index
            current_node['resolution-number'] = successor_index
            current_node['f-cost'] = successor_f_cost
            # the f-limit remains the same

        # check for improvement of the f-limit
        if successor_f_cost <= current_node['f-limit']:
            current_node['f-limit'] = successor_f_cost
            alternative_node['genotype-index'] = successor_genotype_index
            alternative_node['resolution-number'] = successor_genotype_index

    return True


def recursive_breadth_first_search():
    path = () # current set of inferred haplotypes
    while current_node['genotype-index'] < len(genotypes) - 1:
        expand_successors(path)
        print('current node', current_node)
        # permanently addition of the mother haplotype of this resolution to the path
        path = path + (expand_resolution(genotypes[current_node['genotype-index']],
                                         current_node['resolution-number'])[0],)
        # permanently addition of the father haplotype of this resolution to the path
        path = path + (expand_resolution(genotypes[current_node['genotype-index']],
                                         current_node['resolution-number'])[1],)
        print('path', path)

    return path


# extracting the input data
with open("searchSampleInput.txt") as file:
    n, m = [int(x) for x in next(file).split()]
    genotypes = []
    for line in file:  # read rest of lines
        genotypes.append([int(x) for x in line.split()])

    alternative_node = {'genotype-index': -1,
                        'resolution-number': 0}

    current_node = {'genotype-index': -1,
                    'resolution-number': 0,
                    'f-cost': 0,
                    'f-limit': 0}

    print('Search finished with this f-cost: ', len(set(recursive_breadth_first_search())))
