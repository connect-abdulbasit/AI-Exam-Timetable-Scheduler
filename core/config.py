import json
import os
from models import Course, Room, TimeSlot


class Configuration:

    def __init__(self):
        self.courses = []
        self.rooms = []
        self.timeslots = []
        self.student_conflict_groups = []
        self.loaded_from_path = None

    def save_to_file(self, filepath):

        data = {
            "courses": [
                {"id": c.id, "name": c.name, "instructor": c.instructor, "students": c.students_enrolled}
                for c in self.courses
            ],
            "rooms": [{"id": r.id, "capacity": r.capacity} for r in self.rooms],
            "timeslots": [{"id": t.id, "day": t.day, "time": t.time} for t in self.timeslots],
            "student_conflicts": self.student_conflict_groups
        }
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        self.loaded_from_path = os.path.abspath(filepath)

    def load_from_file(self, filepath):

        try:
            with open(filepath, 'r') as f:
                data = json.load(f)

            self.courses = [Course(c["id"], c["name"], c["instructor"], c["students"])
                           for c in data.get("courses", [])]
            self.rooms = [Room(r["id"], r["capacity"]) for r in data.get("rooms", [])]
            self.timeslots = [TimeSlot(t["id"], t["day"], t["time"])
                             for t in data.get("timeslots", [])]
            self.student_conflict_groups = data.get("student_conflicts", [])
            self.loaded_from_path = os.path.abspath(filepath)

            return True, "Configuration loaded successfully"
        except Exception as e:
            return False, f"Error loading configuration: {str(e)}"

    def clear(self):

        self.courses = []
        self.rooms = []
        self.timeslots = []
        self.student_conflict_groups = []
        self.loaded_from_path = None

    def get_course_group(self, course_id):

        for i, group in enumerate(self.student_conflict_groups):
            if course_id in group:
                return i
        return -1

    def validate(self):

        errors = []
        if not self.courses:
            errors.append("At least one course is required")
        if not self.rooms:
            errors.append("At least one room is required")
        if not self.timeslots:
            errors.append("At least one time slot is required")
        return errors
