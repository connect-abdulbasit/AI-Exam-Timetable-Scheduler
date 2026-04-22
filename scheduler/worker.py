import copy
import random
from PyQt5.QtCore import QThread, pyqtSignal
from .engine import GeneticAlgorithm

class GAWorker(QThread):
    progress_update = pyqtSignal(int, float, dict)
    finished_signal = pyqtSignal(dict, float)

    def __init__(self, config):
        super().__init__()
        self.config = config

    def run(self):
        ga = GeneticAlgorithm(self.config)
        population = [ga.generate_chromosome() for _ in range(ga.pop_size)]
        
        generations = 200
        best_overall = None
        best_fitness = 0.0

        for gen in range(generations):
            # Evaluate
            scored = [(ga.calculate_fitness(ind), ind) for ind in population]
            scored.sort(key=lambda x: x[0], reverse=True)
            
            current_best_fit = scored[0][0]
            current_best_ind = scored[0][1]

            if current_best_fit > best_fitness:
                best_fitness = current_best_fit
                best_overall = copy.deepcopy(current_best_ind)

            # Update GUI every 2 generations to save rendering overhead
            if gen % 1 == 0:
                self.progress_update.emit(gen, best_fitness, best_overall)

            # Terminate if perfect
            if best_fitness == 1.0:
                self.progress_update.emit(gen, best_fitness, best_overall)
                break

            # Elitism: Keep top 10% automatically (deepcopy to avoid mutation corruption)
            elite_count = int(ga.pop_size * 0.1)
            next_generation = [copy.deepcopy(ind) for fit, ind in scored[:elite_count]]
            
            # Tournament Selection & Crossover
            while len(next_generation) < ga.pop_size:
                p1 = random.choice(scored[:ga.pop_size//2])[1]
                p2 = random.choice(scored[:ga.pop_size//2])[1]
                child = ga.mutate(ga.crossover(p1, p2))
                next_generation.append(child)
                
            population = next_generation

        self.finished_signal.emit(best_overall, best_fitness)
