import random
from abc import ABC
from typing import List

from schedule import Schedule


class Population(ABC):
    def __init__(self, size: int):
        self.size = size
        self.chromosomes = [Schedule().initialize() for _ in range(size)]


class GeneticAlgorithm:
    generation = 0

    POPULATION_SIZE = 10
    MUTATION_RATE = 0.1
    NUM_OF_ELITE = 2
    CYCLE_ADAPTATION = 5

    def evolve(self, population: Population) -> Population:
        self.generation += 1
        population = self.__crossover_population(population)
        population = self.__mutate_population(population)
        if self.generation % self.CYCLE_ADAPTATION == 0:
            population = self.__adaptive_population(population)
        for chromosome in population.chromosomes: chromosome.calculate_fitness()
        population.chromosomes.sort(key=lambda x: x.get_fitness(), reverse=True)
        return population

    def __crossover_population(self, population: Population) -> Population:
        crossover_population = Population(0)
        for i in range(self.NUM_OF_ELITE):
            crossover_population.chromosomes.append(population.chromosomes[i])
        parent1, parent2 = crossover_population.chromosomes[0:2]
        for _ in range(self.POPULATION_SIZE - self.NUM_OF_ELITE):
            crossover_population.chromosomes.append(self.__crossover_chromosome(parent1, parent2))
        return crossover_population

    def __crossover_chromosome(self, parent1: Schedule, parent2: Schedule) -> Schedule:
        crossover_chromosome = Schedule().initialize()
        for i in range(len(crossover_chromosome.genes)):
            if random.random() > 0.5: crossover_chromosome.genes[i] = parent1.genes[i].copy()
            else: crossover_chromosome.genes[i] = parent2.genes[i].copy()
        crossover_chromosome.calculate_fitness()
        return crossover_chromosome

    def __mutate_population(self, population: Population) -> Population:
        for i in range(self.NUM_OF_ELITE, self.POPULATION_SIZE):
            self.__mutate_chromosome(population.chromosomes[i])
        return population

    def __mutate_chromosome(self, chromosome: Schedule) -> Schedule:
        _chromosome = Schedule().initialize()
        for i in range(len(chromosome.genes)):
            if random.random() < self.MUTATION_RATE: chromosome.genes[i] = _chromosome.genes[i]
        return chromosome

    """
    OUR HEURISTIC
    Sử dụng thêm 1 giai đoạn thích nghi giống sinh học tự nhiên.
    Thay thế những gene không tốt để thích nghi với điều kiện.
    """

    def __adaptive_population(self, population: Population) -> Population:
        for i in range(self.NUM_OF_ELITE, self.POPULATION_SIZE):
            self.__adaptive_chromosome(population.chromosomes[i])
        return population

    def __adaptive_chromosome(self, chromosome: Schedule) -> Schedule:
        _chromosome = Schedule().initialize()
        adap_chromosome = chromosome.copy()
        for i in range(len(chromosome.genes)):
            if chromosome.genes[i].conflict:
                adap_chromosome.genes[i] = _chromosome.genes[i]
                adap_chromosome.calculate_fitness()
                if not adap_chromosome.genes[i].conflict:
                    chromosome.genes[i] = _chromosome.genes[i]
        return chromosome
