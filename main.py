from problem import Problem
from GA import GA
from SA import SA
from constants import (NUM_TESTS, MAX_WEIGHT, ITEMS, NUM_INDIVIDUALS,
                       MAX_GENERATIONS, INITIAL_TEMPERATURE, COOLING_FACTOR,
                       MAX_CYCLES, NEIGHBORS_PER_CYCLE, USE_SWAP)

if __name__ == "__main__":
    problem = Problem(MAX_WEIGHT, ITEMS)

    print("=== Genetic Algorithm ===")
    ga = GA(problem, NUM_INDIVIDUALS, MAX_GENERATIONS)
    ga.startTests(NUM_TESTS)

    print("\n=== Simulated Annealing ===")
    sa = SA(problem, MAX_CYCLES, NEIGHBORS_PER_CYCLE, INITIAL_TEMPERATURE, COOLING_FACTOR, USE_SWAP)
    sa.startTests(NUM_TESTS)
