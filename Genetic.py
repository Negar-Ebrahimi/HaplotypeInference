import random
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


def fitness(individual):
    haplotypes = ()
    for genotype_index in range(len(genotypes)):
        haplotypes = haplotypes + (expand_resolution(genotypes[genotype_index], individual[genotype_index])[0],)  # Add mother
        haplotypes = haplotypes + (expand_resolution(genotypes[genotype_index], individual[genotype_index])[1],)  # Add father

    return 2*len(genotypes) - len(set(haplotypes))


def initial_population():
    population = []
    initial_population_size = 100  # This can be changed
    for index in range(initial_population_size):
        individual = ()
        for genotype in genotypes:
            if resolutions_size(genotype) > 0:
                individual = individual + (random.randint(1, resolutions_size(genotype)) - 1,)
            else:
                individual = individual + (0,)  # This genotype has no recessive allele and has one identical resolution

        population.append(individual)
    return population


def selection():
    most_fit_individual_1_index = -1
    most_fit_individual_1_score = 0

    most_fit_individual_2_index = -1
    most_fit_individual_2_score = 0

    for individual_index in range(len(population)):
        individual = population[individual_index]
        if fitness(individual) > most_fit_individual_1_score:
            most_fit_individual_2_index = most_fit_individual_1_index
            most_fit_individual_2_score = most_fit_individual_1_score
            most_fit_individual_1_index = individual_index
            most_fit_individual_1_score = fitness(individual)

        elif individual_index != most_fit_individual_1_index and fitness(individual) > most_fit_individual_2_score:
            most_fit_individual_2_index = individual_index
            most_fit_individual_2_score = fitness(individual)
    return [population[most_fit_individual_1_index], population[most_fit_individual_2_index]]


def crossover(selected_parents):
    crossover_point = random.randint(0, len(genotypes) - 2)
    offspring_1 = ()
    offspring_2 = ()
    for genotype_index in range(len(genotypes)):
        if genotype_index <= crossover_point:
            offspring_1 = offspring_1 + (selected_parents[1][genotype_index],)
            offspring_2 = offspring_2 + (selected_parents[0][genotype_index],)
        else:
            offspring_1 = offspring_1 + (selected_parents[0][genotype_index],)
            offspring_2 = offspring_2 + (selected_parents[1][genotype_index],)
    # Mutation section
    offspring_1 = mutation(offspring_1)
    offspring_2 = mutation(offspring_2)

    population.append(offspring_1)
    population.append(offspring_2)

    # keep the population size fixed
    kill_the_least_fit()
    kill_the_least_fit()

    return population


def mutation(offspring):
    mutation_probability = 0.30
    number_of_being_mutated_genotypes = 2
    offspring_list = list(offspring)  # We can't change the values of the tuple DS, but the list DS is okay with that
    if random.random() < mutation_probability:
        for iterator in range(number_of_being_mutated_genotypes):
            genotype_index = random.randint(0, len(genotypes) - 1)
            if resolutions_size(genotypes[genotype_index]) > 0:
                offspring_list[genotype_index] = random.randint(1, resolutions_size(genotypes[genotype_index])) - 1
    return tuple(offspring_list)


def kill_the_least_fit():
    least_fit_individual_index = -1
    least_fit_individual_score = 2*len(genotypes)+1

    for individual_index in range(len(population)):
        individual = population[individual_index]
        if fitness(individual) < least_fit_individual_score:
            least_fit_individual_index = individual_index
            least_fit_individual_score = fitness(individual)

    del population[least_fit_individual_index]
    return population


def total_score():
    total_score = 0
    for individual in population:
        total_score += fitness(individual)
    return total_score


def max_fit():
    most_fit_individual_index = -1
    most_fit_individual_score = 0

    for individual_index in range(len(population)):
        individual = population[individual_index]
        if fitness(individual) > most_fit_individual_score:
            most_fit_individual_index = individual_index
            most_fit_individual_score = fitness(individual)
    return population[most_fit_individual_index]

# def is_converged(): ?


answers = []
for l in range(10):
    # extracting the input data
    with open("SmallSampleInput.txt") as file:
        n, m = [int(x) for x in next(file).split()]
        genotypes = []
        for line in file:  # read rest of lines
            genotypes.append([int(x) for x in line.split()])

        population = initial_population()
        max_fit_score = 0
        # population is gonna change globally through every generation

        number_of_generations = 50
        number_of_selections = 5
        i = 1
        for i in range(number_of_generations):
            for r in range(number_of_selections):
                crossover(selection())
                if max_fit_score < fitness(max_fit()):
                    max_fit_score = fitness(max_fit())
        answers.append(2*len(genotypes) - max_fit_score)

print(answers)