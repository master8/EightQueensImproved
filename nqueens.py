import numpy as np
import random


class Solver_8_queens:
    __pop_size = 10
    __cross_prob = 1.0
    __mut_prob = 1.0

    __board_size = 8

    def __init__(self, pop_size=20, cross_prob=1.0, mut_prob=1.0):
        self.__pop_size = pop_size
        self.__cross_prob = cross_prob
        self.__mut_prob = mut_prob

    def solve(self, min_fitness=None, max_epochs=None):
        best_fit = 0.0
        epoch_num = 0

        population = self.__generate_population()

        while best_fit != 1.0:
            if min_fitness is not None and best_fit >= min_fitness:
                break

            if max_epochs is not None and epoch_num >= max_epochs:
                break

            fit_values = self.__count_fit_values(population)
            parents = self.__reproduction(population, fit_values)
            children = self.__crossover(parents)
            self.__mutate(children)
            population, best_fit = self.__select(population, children, fit_values)

            epoch_num += 1

        visualization = self.__generate_visualization(population[len(population) - 1])

        return best_fit, epoch_num, visualization

    def __generate_population(self):
        initial_population = np.zeros((self.__pop_size, self.__board_size), dtype=np.ubyte)

        for chromosome in initial_population:
            for i in range(0, len(chromosome)):
                chromosome[i] = i

            random.shuffle(chromosome)

        return initial_population

    def __count_fit_values(self, population):
        fit_values = np.zeros(len(population))
        for i, chromosome in enumerate(population):
            fit_values[i] = (self.__fit_fun(chromosome))

        return fit_values

    def __reproduction(self, population, fit_values):
        wheel = []

        for index, value in enumerate(fit_values):
            size = int(round(value / np.sum(fit_values) * 100))
            for _ in range(0, size):
                wheel.append(index)

        parents = np.zeros((len(population), self.__board_size), dtype=np.ubyte)

        for i in range(0, len(population)):
            parents[i] = population[wheel[random.randrange(0, len(wheel))]]

        return parents

    def __crossover(self, parents):
        children = np.zeros((int(len(parents)), self.__board_size), dtype=np.ubyte)

        for x in range(0, int(self.__pop_size / 2)):
            if random.randrange(0, 100) < self.__cross_prob * 100:
                y = int(self.__pop_size / 2) + x
                first_parent = parents[x]
                second_parent = parents[y]

                for i in range(0, self.__board_size):
                    children[x][i] = first_parent[second_parent[i]]

        return children

    def __mutate(self, children):
        for chromosome in children:
            if random.randrange(0, 100) < self.__mut_prob * 100:
                bit1 = random.randrange(0, len(chromosome))
                bit2 = random.randrange(0, len(chromosome))
                temp = chromosome[bit1]
                chromosome[bit1] = chromosome[bit2]
                chromosome[bit2] = temp

    def __select(self, population, children, fit_values):
        children_fit_values = self.__count_fit_values(children)
        full_population = np.concatenate((population, children))
        full_fit_values = np.concatenate((fit_values, children_fit_values))

        new_population = full_population[full_fit_values.argsort()][self.__pop_size:]

        return new_population, np.max(full_fit_values)

    def __generate_visualization(self, solution):
        result = ''
        for gen in solution:
            result += '+' * gen + 'Q' + '+' * (self.__board_size - gen - 1) + '\n'

        return result

    def __fit_fun(self, chromosome_int_code):
        count = len(chromosome_int_code) - len(np.unique(chromosome_int_code))

        for x1, y1 in enumerate(chromosome_int_code):
            for x2 in range(x1 + 1, len(chromosome_int_code)):
                if self.__is_diagonal_conflict(x1, y1, x2, chromosome_int_code[x2]):
                    count += 1

        return 1 / (count + 1)

    @staticmethod
    def __is_diagonal_conflict(x1, y1, x2, y2):
        if x1 == x2 or y1 == y2:
            return False
        diff_x = int(x1) - int(x2)
        diff_y = int(y1) - int(y2)
        return abs(diff_x / diff_y) == 1
