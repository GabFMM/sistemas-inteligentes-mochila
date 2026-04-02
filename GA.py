from individual import Individual
from constants import ITEM_CHOSEN_PERCENT, MUTATION_PERCENT
from utils import fractional_knapsack_bound
import random
import time
import itertools

# GA is genetics algorithms 
class GA:
    def __init__(self, problem, numIndividuals, maxGenerations):
        self.problem = problem
        self.numIndividuals = numIndividuals
        self.population = [None for i in range(numIndividuals)]
        self.maxGenerations = maxGenerations
        self.bestIndividual = Individual(len(problem.items))
        self.bestFitness = 0
        self.maxStagnationBestFitness = int(maxGenerations * 0.2)
        self.stagnationBestFitness = 0
        self.mutationExtraPercent = 0

    def restartAlgorithm(self):
        self.population = [None for i in range(self.numIndividuals)]
        self.bestIndividual = Individual(len(self.problem.items))
        self.bestFitness = 0
        self.stagnationBestFitness = 0
        self.mutationExtraPercent = 0

    # only create valid individuals
    # weight individual <= max weight
    def randomizePopulation(self):
        numItems = len(self.problem.items)

        for i in range(self.numIndividuals):
            individual = Individual(numItems)
            self.population[i] = individual

            itemsIndex = list(range(numItems))
            random.shuffle(itemsIndex)

            individualWeight = 0
            for j in itemsIndex:
                item_weight = self.problem.items[j][0] 

                # if the individual can choose de item
                if individualWeight + item_weight <= self.problem.maxWeight and random.random() <= ITEM_CHOSEN_PERCENT:
                    individual.chooseItem(j)
                    individualWeight += item_weight
                elif individualWeight > self.problem.maxWeight:
                    break

    # returns the fitness for each individual and the best individual
    def calculateFitness(self):
        # add an epsilon to random.choices to work
        fitness = [1] * len(self.population)
        bestIndividualFitness = 0
        bestIndividual = None

        for i in range(len(self.population)):
            individual = self.population[i] 
            # calculates the weight and the value
            weight = 0
            value = 1 # add an epsilon to random.choices to work
            for j in range(len(individual.representation)):
                if individual.representation[j]:
                    weight += self.problem.items[j][0]
                    value += self.problem.items[j][1]

            # jumps to the next individual
            if weight < self.problem.maxWeight:
                fitness[i] = value
            else:
                excess = weight - self.problem.maxWeight
                fitness[i] = value / (1 + excess) # plus 1 to avoid division by 0
            
            if fitness[i] > bestIndividualFitness:
                bestIndividualFitness = fitness[i]
                bestIndividual = individual

        return fitness, bestIndividual
 
    # this method does crossover and mutation across two individuals
    # returns a pair of individuals
    def reproduction(self, x, y):
        # crossover
        cutoffNum = random.randint(0, len(x.representation))
        newIndivualA = self.crossover(x, y, cutoffNum)
        newIndivualB = self.crossover(y, x, cutoffNum)

        # mutation
        self.mutation(newIndivualA)
        self.mutation(newIndivualB)

        return [newIndivualA, newIndivualB]

    # The order between x and y indivuals matters
    # The new individual will receive first part of x and after part of y
    def crossover(self, x, y, cutoffNum):
        representationPartX = [x.representation[i] for i in range(cutoffNum)]
        representationPartY = [y.representation[i] for i in range(cutoffNum, len(x.representation))]
        return Individual(len(x.representation), [representationPartX, representationPartY])
    
    def mutation(self, individual):
        for i in range(len(individual.representation)):
            if random.random() <= MUTATION_PERCENT * (1 + self.mutationExtraPercent):
                individual.representation[i] = not individual.representation[i]

    def startDefault(self):
        start_time = time.perf_counter()

        self.randomizePopulation()
        fitness, self.bestIndividual = self.calculateFitness()
        self.bestFitness = max(fitness)

        generations = 0
        while generations < self.maxGenerations and self.stagnationBestFitness < self.maxStagnationBestFitness:
            generations += 1

            cumWeights = list(itertools.accumulate(fitness))
            newPopulation = []
            for _ in range(0, self.numIndividuals, 2):
                pair = random.choices(self.population, cum_weights=cumWeights, k=2)
                newIndividuals = self.reproduction(pair[0], pair[1])
                newPopulation.extend(newIndividuals)
            newPopulation[0] = self.bestIndividual

            self.population = newPopulation
            fitness, bestIndividualCandidate = self.calculateFitness()

            currentBest = max(fitness)
            if currentBest > self.bestFitness:
                self.bestFitness = currentBest
                self.bestIndividual = bestIndividualCandidate
                self.stagnationBestFitness = 0
                self.mutationExtraPercent = 0
            else:
                self.stagnationBestFitness += 1
                self.mutationExtraPercent += 0.001

        end_time = time.perf_counter()
        elapsed_time = end_time - start_time

        return generations, elapsed_time

    def startTests(self, numTests):
        sumElapsedTime = 0
        sumGenerations = 0
        sumQualitys = 0

        maxValuePossible = fractional_knapsack_bound(self.problem.items, self.problem.maxWeight)

        for i in range(numTests):
            print(f"Test: {i + 1}")

            generations, elapsed_time = self.startDefault()

            sumGenerations += generations
            sumElapsedTime += elapsed_time
            # must remove epsilon (1)
            sumQualitys += (self.bestFitness - 1) / maxValuePossible 

            self.restartAlgorithm()

        print(f"Average elapsed time: {sumElapsedTime/numTests:.4f} seconds")
        print(f"Average generations ocurred: {int(sumGenerations/numTests)} of {self.maxGenerations}")
        print(f"Average quality: {sumQualitys/numTests:.4f}")

    def start(self):
        generations, elapsed_time = self.startDefault()

        print(f"Elapsed time: {elapsed_time:.4f} seconds")
        print(f"Generations ocurred: {generations} of {self.maxGenerations}")
        print(f"Best value: {self.bestFitness - 1}") # must remove epsilon
        print(f"Best individual:\n{self.bestIndividual.representation}")               