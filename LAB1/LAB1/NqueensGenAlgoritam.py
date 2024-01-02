import random
import time



def random_chromosome(size):  # making random chromosomes
    return [random.randint(1, nq) for _ in range(nq)]

def fitness(chromosome):
    horizontal_collisions = sum([chromosome.count(queen) - 1 for queen in chromosome]) / 2
    diagonal_collisions = 0

    n = len(chromosome)
    left_diagonal = [0] * 2 * n
    right_diagonal = [0] * 2 * n
    for i in range(n):
        left_diagonal[i + chromosome[i] - 1] += 1
        right_diagonal[len(chromosome) - i + chromosome[i] - 2] += 1

    diagonal_collisions = 0
    for i in range(2 * n - 1):
        counter = 0
        if left_diagonal[i] > 1:
            counter += left_diagonal[i] - 1
        if right_diagonal[i] > 1:
            counter += right_diagonal[i] - 1
        diagonal_collisions += counter / (n - abs(i - n + 1))

    return int(maxFitness - (2*horizontal_collisions + diagonal_collisions))
    # kažnjavamo jače ako dolazi do horizontalne/okomite kolizije


def probability(chromosome, fitness):
    return fitness(chromosome) / maxFitness


def random_pick(population, probabilities):
    populationWithProbabilty = zip(population, probabilities)
    total = sum(w for c, w in populationWithProbabilty)
    r = random.uniform(0, total)
    upto = 0
    for c, w in zip(population, probabilities):
        if upto + w >= r:
            return c
        upto += w
    assert False, "Shouldn't get here"


def reproduce(x, y):  # one point chromosome recombination
    n = len(x)
    c = random.randint(0, n - 1)
    return x[0:c] + y[c:n]


def reproduce2(x, y): # two point chromosome recombination
    n = len(x)
    c = random.randint(0, n - 1)
    c2 = random.randint(c, n - 1)
    return x[0:c] + y[c:c2] + x[c2:n]


def mutate(x):  # randomly changing the value of a random index of a chromosome
    n = len(x)
    c = random.randint(0, n - 1)
    m = random.randint(1, n)
    x[c] = m
    return x


def perMutate(x): #permutacija
    n = len(x)
    c = random.randint(0, n-1)
    c2 = random.randint(0, n-1)
    f = x[c]
    x[c]=x[c2]
    x[c2] = f
    return x


def mySort(list , eliteNum):
   counter = 1
   while counter > 0:
       counter = 0
       for i in range(len(list)-1):
           if(fitness(list[i]) < fitness(list[i+1])):
               temp = list[i]
               list[i] = list[i+1]
               list[i+1] = temp
               counter += 1
   return list[0:eliteNum]



def genetic_queen(population, fitness):
    mutation_probability = 0.3
    new_population = []
    probabilities = [probability(n, fitness) for n in population]
    for i in range(len(population)):
        x = random_pick(population, probabilities)  # best chromosome 1
        y = random_pick(population, probabilities)  # best chromosome 2
        child = reproduce2(x, y)
        if random.random() < mutation_probability:
            child = mutate(child)
        print_chromosome(child)
        new_population.append(child)
        if fitness(child) == maxFitness: break
    return new_population


def elit_genetic_queen(population, fitness):
    mutation_probability = 0.3
    eliteNum = 10
    new_population = []
    elitePopulation = mySort(population, eliteNum)

    for r in elitePopulation:
        new_population.append(r)

    probabilities = [probability(n, fitness) for n in population]
    for i in range(len(population)-eliteNum):
        x = random_pick(population, probabilities)  # best chromosome 1
        y = random_pick(population, probabilities)  # best chromosome 2
        child = reproduce2(x, y)
        if random.random() < mutation_probability:
            child = mutate(child)
        print_chromosome(child)
        new_population.append(child)
        if fitness(child) == maxFitness: break
    return new_population


def print_chromosome(chrom):
    print("Chromosome = {},  Fitness = {}"
          .format(str(chrom), fitness(chrom)))


def print_board(board):
    for row in board:
        print(" ".join(row))


if __name__ == "__main__":
    nq = int(input("Enter Number of Queens: "))  # say N = 8
    start = time.time()
    maxFitness = (nq * (nq - 1)) / 2  # 8*7/2 = 28
    print(maxFitness)
    population = [random_chromosome(nq) for _ in range(150)]
    solved = False
    generation = 1
    z = 0

    while not maxFitness  in [fitness(chrom) for chrom in population]:
        print("=== Generation {} ===".format(generation))
        population = genetic_queen(population, fitness)
        print("")
        print("Maximum Fitness = {}".format(max([fitness(n) for n in population])))
        generation += 1
        #ovdje možemo ograničiti broj generacija
        #if generation > 1000:
            #z = 5
            #break
    if(z==0):
        chrom_out = []
        print("Solved in Generation {}!".format(generation - 1))
        for chrom in population:
            if fitness(chrom) == maxFitness:
                print("");
                print("One of the solutions: ")
                chrom_out = chrom
                print_chromosome(chrom)

        board = []

        for x in range(nq):
            board.append([" . "] * nq)

        for i in range(nq):
            board[nq - chrom_out[i]][i] = " Q "
        print()
        print_board(board)
    else:
        print("Nema rjesenja")
    end = time.time()
    print("Time:")
    print(round((end - start),4))
