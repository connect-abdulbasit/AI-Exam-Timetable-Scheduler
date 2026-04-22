import json
import os
from ..models import Course, Room, TimeSlot

class Configuration:

    def __init__(self):
        self.courses = []
        self.rooms = []
        self.timeslots = []
        self.student_conflict_groups = []
        self.load_defaults()

    def load_defaults(self):

        base_path = os.path.dirname(os.path.dirname(__file__))
        default_path = os.path.join(base_path, "data", "default_config.json")

        if os.path.exists(default_path):
            self.load_from_file(default_path)
        else:

            self.courses = [
                Course("C1", "AI", "Dr. Smith", 40), Course("C2", "Data Structures", "Dr. Jones", 55),
                Course("C3", "Database", "Dr. Smith", 35), Course("C4", "Web Dev", "Prof. Alan", 60),
                Course("C5", "OS", "Dr. Brown", 45), Course("C6", "Networks", "Dr. Jones", 50),
                Course("C7", "Calculus", "Prof. White", 100), Course("C8", "Physics", "Dr. Green", 80)
            ]
            self.rooms = [Room("R1", 50), Room("R2", 60), Room("R3", 120)]
            self.timeslots = [
                TimeSlot("T1", "Monday", "09:00 AM"), TimeSlot("T2", "Monday", "02:00 PM"),
                TimeSlot("T3", "Tuesday", "09:00 AM"), TimeSlot("T4", "Tuesday", "02:00 PM"),
                TimeSlot("T5", "Wednesday", "09:00 AM")
            ]
            self.student_conflict_groups = [
                ["C1", "C2", "C5"], ["C3", "C4"], ["C7", "C8"]
            ]

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

            return True, "Configuration loaded successfully"
        except Exception as e:
            return False, f"Error loading configuration: {str(e)}"

    def clear(self):

        self.courses = []
        self.rooms = []
        self.timeslots = []
        self.student_conflict_groups = []

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
