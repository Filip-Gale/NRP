import random
import time
import winsound


note="EDCDEEEDDDEGGEDCDEEEDDDEGG"

#melodija1="EDCDEEEDDDEGG"
#melodija2="EDCDEEEDDDEGGEDCDEEEDDDEGG"


def play_note(znak):
    if (znak == "A"):
        winsound.Beep(440, 1000)
        time.sleep(5 / 1000)
        print("A")
    elif (znak == "B"):
        winsound.Beep(493, 1000)
        time.sleep(5 / 1000)
        print("B")
    elif (znak == "C"):
        winsound.Beep(261, 1000)
        time.sleep(5 / 1000)
        print("C")
    elif (znak == "D"):
        winsound.Beep(293, 1000)
        time.sleep(5 / 1000)
        print("D")
    elif (znak == "E"):
        winsound.Beep(329, 1000)
        time.sleep(5 / 1000)
        print("E")
    elif (znak == "F"):
        winsound.Beep(349, 1000)
        time.sleep(5 / 1000)
        print("F")
    elif (znak == "G"):
        winsound.Beep(392, 1000)
        time.sleep(5 / 1000)
        print("G")


def random_chromosome(size):  # making random chromosomes
    return [random.choice("ABCDEFG") for _ in range(nq)]

def fitness(chromosome1):
    n = len(chromosome1)
    br=0
    for i in range(n):
        if(chromosome1[i]==note[i]):
            #print(chromosome1[i]," ",note[i]," ",i+1)
            br=br+1;
    return int(br)



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
    m = random.choice("ABCDEFG")
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
        child = reproduce(x, y)
        if random.random() < mutation_probability:
            child = perMutate(child)
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
            child = perMutate(child)
        print_chromosome(child)
        new_population.append(child)
        if fitness(child) == maxFitness: break
    return new_population


def print_chromosome(chrom):
    print("Chromosome = {},  Fitness = {}"
          .format(str(chrom), fitness(chrom)))


if __name__ == "__main__":
    nq = len(note)
    start = time.time()
    maxFitness = nq
    print(maxFitness)
    population = [random_chromosome(nq) for _ in range(75)]
    solved = False
    generation = 1
    z = 0
    maximalniDostignutiFitnes=0

    while not maxFitness  in [fitness(chrom) for chrom in population]:
        print("=== Generation {} ===".format(generation))
        population = elit_genetic_queen(population, fitness)
        print("")
        print("Maximum Fitness = {}".format(max([fitness(n) for n in population])))
        generation += 1

#Kod pomoću kojeg možemo čuti kako program napreduje prema boljem rješenju, radi mjerenja je zakomentiran
       #for z in range(len(population)):
            #if(fitness(population[z])==max([fitness(n) for n in population])):
                #if (max([fitness(n) for n in population])>maximalniDostignutiFitnes):
                    #for j in range(len(note)):
                        #play_note(population[z][j])
                #break
        #maximalniDostignutiFitnes=max([fitness(n) for n in population])


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
                end = time.time()
                print("Time:")
                print(round((end - start), 4))
                for i in range(len(chrom)):
                    play_note(chrom[i])

    else:
        end = time.time()
        print("Time:")
        print(round((end - start), 4))

    #end = time.time()
    #print("Time:")
    #print(round((end - start),4))