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


def expand_successors(node):
    successor_genotype_index = node['genotype-index'] + 1
    being_expanded_genotype = genotypes[successor_genotype_index]

    successors = ()
    for successor_index in range(resolutions_size(being_expanded_genotype)):
        # reset current haplotypes
        current_haplotypes = node['path']

        # temporary addition of the mother haplotype of this resolution to the path
        current_haplotypes = current_haplotypes + (expand_resolution(being_expanded_genotype, successor_index)[0],)

        # temporary addition of the father haplotype of this resolution to the path
        current_haplotypes = current_haplotypes + (expand_resolution(being_expanded_genotype, successor_index)[1],)

        # check for improvement of f-cost
        successor_g_cost = path_cost_coefficient*(successor_genotype_index + 1)
        successor_heuristic_value = 2*(len(genotypes) - 1 - successor_genotype_index) + len(set(current_haplotypes))
        successor_f_cost = successor_g_cost + successor_heuristic_value

        successor = {'genotype-index': successor_genotype_index,
                     'resolution-number': successor_index,
                     'path': current_haplotypes,
                     'f-cost': successor_f_cost}
        successors = successors + (successor, )

    return successors


def best_successor_index(successors):
    best_successor_index = 0
    for successor_index in range(len(successors)):
        # This successor is better than current best
        if successors[successor_index]['f-cost'] < successors[best_successor_index]['f-cost']:
            best_successor_index = successor_index
    return best_successor_index


def alternative_successor(successors):
    best_successor = successors[best_successor_index(successors)]
    alternative_successor_index = len(successors) - best_successor_index(successors) - 1
    for successor_index in range(len(successors)):
        # This successor is better than current best
        if successors[successor_index]['f-cost'] < best_successor['f-cost']\
                and successor_index != best_successor_index:
            alternative_successor_index = successor_index
    return successors[alternative_successor_index]


def recursive_breadth_first_search(node, f_limit):
    if node['genotype-index'] == len(genotypes) - 1:
        return ['success', node]

    successors = expand_successors(node)
    while 1:
        best = successors[best_successor_index(successors)]
        if best['f-cost'] > f_limit:
            return ['failure', best]
        alternative = alternative_successor(successors)
        result = recursive_breadth_first_search(best, min(f_limit, alternative['f-cost']))
        unwinding_node = result[1]
        successors_list = list(successors)
        successors_list[best_successor_index(successors)] = unwinding_node
        successors = tuple(successors_list)
        if result[0] == 'success':
            return result


# ToDo: increasing the value of this path cost coefficient makes g greater and therefore,
# the exploration approaches to a more BFS-like process than a DFS-like one.
path_cost_coefficient = 1

# extracting the input data
with open("searchSampleInput.txt") as file:
    n, m = [int(x) for x in next(file).split()]
    genotypes = []
    for line in file:  # read rest of lines
        genotypes.append([int(x) for x in line.split()])

    initial_node = {'genotype-index': -1,
                    'resolution-number': 0,
                    'path': (),
                    'f-cost': 4*len(genotypes)}

    # (path_cost_coefficient+3)*len(genotype) is used as an infinity value for initial f-limit
    initial_f_limit = (path_cost_coefficient + 3)*len(genotypes)

    final_haplotypes_set = set(recursive_breadth_first_search(initial_node, initial_f_limit)[1]['path'])
    print('The minimum-sized inferred haplotypes set is: ', set(final_haplotypes_set))
    print('Number of haplotypes is: ', len(final_haplotypes_set))
