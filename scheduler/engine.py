import random
import copy
from collections import Counter

class GeneticAlgorithm:
    def __init__(self, config, pop_size=100, mutation_rate=0.05):
        self.courses = config.courses
        self.rooms = config.rooms
        self.timeslots = config.timeslots
        self.student_conflict_groups = config.student_conflict_groups
        self.pop_size = pop_size
        self.mutation_rate = mutation_rate

    def generate_chromosome(self):
        # Chromosome: {course_id: (room_id, timeslot_id)}
        timetable = {}
        for c in self.courses:
            timetable[c.id] = (random.choice(self.rooms).id, random.choice(self.timeslots).id)
        return timetable

    def calculate_fitness(self, timetable):
        conflicts = 0
        
        # Maps to track usage for fast conflict checking
        room_time_tracker = set()
        instructor_time_tracker = set()
        course_map = {c.id: c for c in self.courses}
        room_map = {r.id: r for r in self.rooms}

        for course_id, (room_id, timeslot_id) in timetable.items():
            course = course_map[course_id]
            room = room_map[room_id]
            
            # Constraint 1: Room Double Booking
            rt_key = f"{room_id}-{timeslot_id}"
            if rt_key in room_time_tracker:
                conflicts += 1
            room_time_tracker.add(rt_key)
            
            # Constraint 2: Room Capacity
            if course.students_enrolled > room.capacity:
                conflicts += 1
                
            # Constraint 3: Instructor Double Booking
            it_key = f"{course.instructor}-{timeslot_id}"
            if it_key in instructor_time_tracker:
                conflicts += 1
            instructor_time_tracker.add(it_key)

        # Constraint 4: Student Group Conflicts
        for group in self.student_conflict_groups:
            group_times = [timetable[cid][1] for cid in group if cid in timetable]
            # Count actual duplicates
            time_counts = Counter(group_times)
            for count in time_counts.values():
                if count > 1:
                    conflicts += count - 1  # each extra is a conflict

        # Fitness formula (Max 1.0 = Perfect Schedule)
        return 1.0 / (1.0 + conflicts)

    def crossover(self, parent1, parent2):
        # Single-point crossover
        child = {}
        crossover_point = random.randint(1, len(self.courses) - 1)
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
