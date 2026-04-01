from constants import ITEM_CHOSEN_PERCENT
from utils import fractional_knapsack_bound
import random
import time
import math

# SA is simulated annealing
# for solving the 0/1 knapsack problem using local search with
# probabilistic acceptance of worse solutions to escape local optima
class SA:
    # the knapsack problem instance (max weight and items)
    # maxCycles: number of outer loop iterations (temperature decay steps)
    # neighborsPerCycle: number of neighbor attempts per temperature level
    # initialTemp: starting temperature, this controls the initial acceptance of worse solutions. It's better to accept more risk
    # at the start
    # coolingFactor: rate of temperature decay (T = T * coolingFactor each cycle)
    # useSwap: if True, uses swap neighborhood instead of bit-flip, needed for comparison with flip vs swap
    def __init__(self, problem, maxCycles, neighborsPerCycle, initialTemp, coolingFactor, useSwap):
        self.problem = problem
        self.maxCycles = maxCycles
        self.neighborsPerCycle = neighborsPerCycle
        self.initialTemp = initialTemp
        self.coolingFactor = coolingFactor
        self.useSwap = useSwap
        self.currentSolution = None
        self.currentValue = 0
        self.bestSolution = None
        self.bestValue = 0

    # resets the algorithm state to allow a new execution
    def restartAlgorithm(self):
        self.currentSolution = None
        self.currentValue = 0
        self.bestSolution = None
        self.bestValue = 0

    # returns the total weight of a solution
    # sums the weight of each selected item, will be True in the boolean array
    def calculateWeight(self, solution):
        weight = 0
        for j in range(len(solution)):
            if solution[j]:
                weight += self.problem.items[j][0]
        return weight

    # returns the total value of a solution
    # sums the value of each selected item, will be True in the boolean array
    def calculateValue(self, solution):
        value = 0
        for j in range(len(solution)):
            if solution[j]:
                value += self.problem.items[j][1]
        return value

    # generates a random valid initial solution
    # iterates items in random order and selects each with a probability
    # ensuring the total weight does not exceed the knapsack capacity
    def randomizeSolution(self):
        numItems = len(self.problem.items)
        solution = [False] * numItems

        itemsIndex = list(range(numItems))
        random.shuffle(itemsIndex)

        solutionWeight = 0
        for j in itemsIndex:
            item_weight = self.problem.items[j][0]

            # if the solution can choose the item
            if solutionWeight + item_weight <= self.problem.maxWeight and random.random() <= ITEM_CHOSEN_PERCENT:
                solution[j] = True
                solutionWeight += item_weight
            elif solutionWeight > self.problem.maxWeight:
                break

        self.currentSolution = solution
        self.currentValue = self.calculateValue(solution)
        self.bestSolution = list(solution)
        self.bestValue = self.currentValue

    # generates a neighbor by flipping a single random bit
    # this adds or removes one item from the solution using small pertubation
    def generateNeighborFlip(self):
        neighbor = list(self.currentSolution)
        index = random.randint(0, len(neighbor) - 1)
        neighbor[index] = not neighbor[index]
        return neighbor

    # generates a neighbor by swapping one selected item for one unselected item
    # removes a random True item and adds a random False item
    # maintains the same number of items, tending to keep weight stable
    # falls back to flip if all items are selected or none are
    def generateNeighborSwap(self):
        neighbor = list(self.currentSolution)
        trueIndices = [i for i in range(len(neighbor)) if neighbor[i]]
        falseIndices = [i for i in range(len(neighbor)) if not neighbor[i]]

        if len(trueIndices) == 0 or len(falseIndices) == 0:
            return self.generateNeighborFlip()

        trueIndex = random.choice(trueIndices)
        falseIndex = random.choice(falseIndices)
        neighbor[trueIndex] = False
        neighbor[falseIndex] = True
        return neighbor

    # dispatches neighbor generation based on the useSwap flag
    def generateNeighbor(self):
        if self.useSwap:
            return self.generateNeighborSwap()
        else:
            return self.generateNeighborFlip()

    # outer loop: controls the temperature decay across maxCycles iterations
    # inner loop: explores neighborsPerCycle neighbors at each temperature level
    # acceptance criteria:
    #   - if the neighbor is better (deltaE > 0): always accept
    #   - if the neighbor is worse (deltaE <= 0): accept with probability e^(deltaE/T)
    #     this probability decreases as temperature drops, reducing exploration over time
    # invalid neighbors are rejected immediately
    # the best solution found across all iterations is tracked separately
    def startDefault(self):
        start_time = time.perf_counter()

        # step 1: generate a random valid initial solution
        self.randomizeSolution()
        temperature = self.initialTemp
        cycles = 0

        # step 2: outer loop - each iteration represents one temperature level
        while cycles < self.maxCycles:
            cycles += 1

            # step 3: inner loop - explore neighbors at the current temperature
            for _ in range(self.neighborsPerCycle):
                neighbor = self.generateNeighbor()
                neighborWeight = self.calculateWeight(neighbor)

                # reject invalid neighbors that exceeds knapsack capacity
                if neighborWeight > self.problem.maxWeight:
                    continue

                neighborValue = self.calculateValue(neighbor)
                # deltaE is the difference in value between neighbor and current
                deltaE = neighborValue - self.currentValue

                if deltaE > 0:
                    # better solution: always accept
                    self.currentSolution = neighbor
                    self.currentValue = neighborValue
                else:
                    # worse solution: accept with probability e^(deltaE/T)
                    # at high T, probability is close to 1 (explores freely)
                    # at low T, probability approaches 0 (converges to best)
                    probability = math.exp(deltaE / temperature)
                    if random.random() < probability:
                        self.currentSolution = neighbor
                        self.currentValue = neighborValue

                # track the global best solution found
                if self.currentValue > self.bestValue:
                    self.bestValue = self.currentValue
                    self.bestSolution = list(self.currentSolution)

            # step 4: geometric cooling schedule - reduce temperature
            # T_new = T_old * coolingFactor (e.g. 0.99)
            temperature = temperature * self.coolingFactor

        end_time = time.perf_counter()
        elapsed_time = end_time - start_time

        return cycles, elapsed_time

    # runs multiple tests and calculates average metrics
    # compares the best value found against the optimal solution via dynamic proggraming
    # quality = bestValue / optimalValue 
    def startTests(self, numTests):
        sumElapsedTime = 0
        sumCycles = 0
        sumQualitys = 0

        maxValuePossible = fractional_knapsack_bound(self.problem.items, self.problem.maxWeight)

        for i in range(numTests):
            print(f"Test: {i + 1}")

            cycles, elapsed_time = self.startDefault()

            sumCycles += cycles
            sumElapsedTime += elapsed_time
            sumQualitys += self.bestValue / maxValuePossible

            self.restartAlgorithm()

        print(f"Average elapsed time: {sumElapsedTime/numTests:.4f} seconds")
        print(f"Average cycles ocurred: {int(sumCycles/numTests)} of {self.maxCycles}")
        print(f"Average quality: {sumQualitys/numTests:.4f}")

    # runs a single execution and prints the results
    def start(self):
        cycles, elapsed_time = self.startDefault()

        print(f"Elapsed time: {elapsed_time:.4f} seconds")
        print(f"Cycles ocurred: {cycles} of {self.maxCycles}")
        print(f"Best value: {self.bestValue}")
        print(f"Best solution:\n{self.bestSolution}")
