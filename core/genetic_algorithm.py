import random
import copy
from collections import Counter
from PyQt5.QtCore import QThread, pyqtSignal

class GeneticAlgorithm:
    def __init__(self, config, pop_size=100, mutation_rate=0.05):
        self.courses = config.courses
        self.rooms = config.rooms
        self.timeslots = config.timeslots
        self.student_conflict_groups = config.student_conflict_groups
        self.pop_size = pop_size
        self.mutation_rate = mutation_rate

    def generate_chromosome(self):

        timetable = {}
        for c in self.courses:
            timetable[c.id] = (random.choice(self.rooms).id, random.choice(self.timeslots).id)
        return timetable

    def calculate_fitness(self, timetable):
        conflicts = 0

        room_time_tracker = set()
        instructor_time_tracker = set()
        course_map = {c.id: c for c in self.courses}
        room_map = {r.id: r for r in self.rooms}

        for course_id, (room_id, timeslot_id) in timetable.items():
            course = course_map[course_id]
            room = room_map[room_id]

            rt_key = f"{room_id}-{timeslot_id}"
            if rt_key in room_time_tracker:
                conflicts += 1
            room_time_tracker.add(rt_key)

            if course.students_enrolled > room.capacity:
                conflicts += 1

            it_key = f"{course.instructor}-{timeslot_id}"
            if it_key in instructor_time_tracker:
                conflicts += 1
            instructor_time_tracker.add(it_key)

        for group in self.student_conflict_groups:
            group_times = [timetable[cid][1] for cid in group if cid in timetable]

            time_counts = Counter(group_times)
            for count in time_counts.values():
                if count > 1:
                    conflicts += count - 1

        return 1.0 / (1.0 + conflicts)

    def crossover(self, parent1, parent2):

        child = {}
        if not self.courses: return child
        crossover_point = random.randint(0, len(self.courses) - 1)
        course_ids = [c.id for c in self.courses]

        for i, cid in enumerate(course_ids):
            if i < crossover_point:
                child[cid] = parent1[cid]
            else:
                child[cid] = parent2[cid]
        return child

    def mutate(self, timetable):
        for cid in timetable:
            if random.random() < self.mutation_rate:
                timetable[cid] = (random.choice(self.rooms).id, random.choice(self.timeslots).id)
        return timetable

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

            scored = [(ga.calculate_fitness(ind), ind) for ind in population]
            scored.sort(key=lambda x: x[0], reverse=True)

            current_best_fit = scored[0][0]
            current_best_ind = scored[0][1]

            if current_best_fit > best_fitness:
                best_fitness = current_best_fit
                best_overall = copy.deepcopy(current_best_ind)

            self.progress_update.emit(gen, best_fitness, best_overall)

            if best_fitness == 1.0:
                break

            elite_count = int(ga.pop_size * 0.1)
            next_generation = [copy.deepcopy(ind) for fit, ind in scored[:elite_count]]

            while len(next_generation) < ga.pop_size:
                p1 = random.choice(scored[:ga.pop_size//2])[1]
                p2 = random.choice(scored[:ga.pop_size//2])[1]
                child = ga.mutate(ga.crossover(p1, p2))
                next_generation.append(child)

            population = next_generation

        self.finished_signal.emit(best_overall, best_fitness)
