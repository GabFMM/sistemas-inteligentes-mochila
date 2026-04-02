import argparse
from problem import Problem
from GA import GA
from SA import SA
from constants import (NUM_TESTS, MAX_WEIGHT, ITEMS, NUM_INDIVIDUALS,
                       MAX_GENERATIONS, INITIAL_TEMPERATURE, COOLING_FACTOR,
                       MAX_CYCLES, NEIGHBORS_PER_CYCLE, USE_SWAP, MUTATION_PERCENT)

def startSA():
    problem = Problem(MAX_WEIGHT, ITEMS)

    print("\n=== Simulated Annealing ===")
    sa = SA(problem, MAX_CYCLES, NEIGHBORS_PER_CYCLE, INITIAL_TEMPERATURE, COOLING_FACTOR, USE_SWAP)

    if(NUM_TESTS <= 0):
        sa.start()
    else:
        sa.startTests(NUM_TESTS)

def startGA():
    problem = Problem(MAX_WEIGHT, ITEMS)

    print("=== Genetic Algorithm ===")
    ga = GA(problem, NUM_INDIVIDUALS, MAX_GENERATIONS)
    
    if(NUM_TESTS <= 0):
        ga.start()
    else:
        ga.startTests(NUM_TESTS)

def startAll():
    problem = Problem(MAX_WEIGHT, ITEMS)

    print("=== Genetic Algorithm ===")
    ga = GA(problem, NUM_INDIVIDUALS, MAX_GENERATIONS)
    
    if(NUM_TESTS <= 0):
        ga.start()
    else:
        ga.startTests(NUM_TESTS)

    print("\n=== Simulated Annealing ===")
    sa = SA(problem, MAX_CYCLES, NEIGHBORS_PER_CYCLE, INITIAL_TEMPERATURE, COOLING_FACTOR, USE_SWAP)
    
    if(NUM_TESTS <= 0):
        sa.start()
    else:
        sa.startTests(NUM_TESTS)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--alg", choices=["SA", "GA", "ALL"], default="ALL", help="algorithm name (SA or GA or ALL)")
    args = parser.parse_args()

    match args.alg:
        case "SA":
            startSA()
        case "GA":
            startGA()
        case "ALL":
            startAll()