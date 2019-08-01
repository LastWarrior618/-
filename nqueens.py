import random


class Solver_8_queens:

    def __init__(self, pop_size=150, cross_prob=0.75, mut_prob=0.2):
        self.MAX_CROSS = 8 * (8 - 1) // 2
        self.population = []
        self.fitness = [0] * pop_size
        self.pop_size = pop_size
        self.cross_prob = cross_prob
        self.mut_prob = mut_prob

        self.init_pop()

    def init_pop(self):
        """ Инициализация популяции """
        for i in range(self.pop_size):
            chroma = list(range(8))
            random.shuffle(chroma)
            self.population.append(chroma)
            self.update_fitness(i)

    def update_fitness(self, k):
        """ Обновляет значение фитнесс-функции для k-той хромосомы """
        crossings = 0
        for i in range(8):
            for j in range(i + 1, 8):
                diff = self.population[k][i] - self.population[k][j]
                if abs(diff) == abs(i - j):
                    crossings += 1
        self.fitness[k] = self.MAX_CROSS - crossings

    def reproduce(self):
        """ Реализация этапа репродукции """
        self.population, pop_2 = [], self.population
        self.fitness, fit_2 = [], self.fitness
        total_fit = sum(fit_2)
        while len(self.population) != len(pop_2):
            rand = random.randrange(total_fit)
            wheel = 0
            for i in range(len(pop_2)):
                if rand <= wheel:
                    self.population.append(list(pop_2[i]))
                    self.fitness.append(fit_2[i])
                    break
                wheel += fit_2[i]

    def crossingover(self):
        """ Реализация этапа скрещивания """
        if random.random() < self.cross_prob:
            k1 = random.randrange(len(self.population))
            k2 = random.randrange(len(self.population))
            if k1 != k2:
                k = random.randrange(len(self.population) - 1) + 1
                pop1 = self.population[k1]
                pop2 = self.population[k2]
                self.population[k1] = list(pop1[:k] + pop2[k:])
                self.population[k2] = list(pop2[:k] + pop1[k:])
                self.update_fitness(k1)
                self.update_fitness(k2)

    def mutation(self):
        """ Реализация этапа мутации """
        for i in range(len(self.population)):
            if random.random() < self.mut_prob:
                k1 = random.randrange(8)
                k2 = random.randrange(8)
                pop = self.population[i]
                pop[k1], pop[k2] = pop[k2], pop[k1]
                self.update_fitness(i)

    def find_best(self):
        best = self.fitness[0]
        best_k = 0
        for i in range(1, len(self.population)):
            if best < self.fitness[i]:
                best = self.fitness[i]
                best_k = i
        return best_k, best

    def visual(self, k):
        """ Преобразование k-той хромосомы в строку для визуализации """
        visual_str = [['+' for i in range(8)] for i in range(8)]
        for i in range(8):
            visual_str[i][self.population[k][i]] = 'Q'
        for i in range(len(visual_str)):
            visual_str[i] = ''.join(visual_str[i])
        return '\n'.join(visual_str)

    def solve(self, min_fitness=0.99, max_epochs=500):
        epochs = 0
        best_k, best = self.find_best()
        while (max_epochs is None) or (epochs < max_epochs):
            if (min_fitness is not None and
                    best >= self.MAX_CROSS * min_fitness):
                break
            self.reproduce()
            self.crossingover()
            self.mutation()
            best_k, best = self.find_best()
            epochs += 1

        # best fit, epochs, visualization
        return best / self.MAX_CROSS, epochs, self.visual(best_k)
