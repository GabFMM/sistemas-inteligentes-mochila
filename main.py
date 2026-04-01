from problem import Problem
from GA import GA
from constants import NUM_TESTS, MAX_WEIGHT, ITEMS, NUM_INDIVIDUALS, MAX_GENERATIONS

if __name__ == "__main__":
    problem = Problem(MAX_WEIGHT, ITEMS)
    algorithm = GA(problem, NUM_INDIVIDUALS, MAX_GENERATIONS)
    algorithm.startTests(NUM_TESTS)