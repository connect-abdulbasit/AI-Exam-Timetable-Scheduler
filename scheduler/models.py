class Course:
    def __init__(self, id, name, instructor, students_enrolled):
        self.id = id
        self.name = name
        self.instructor = instructor
        self.students_enrolled = students_enrolled # Count of students

class Room:
    def __init__(self, id, capacity):
        self.id = id
        self.capacity = capacity

class TimeSlot:
    def __init__(self, id, day, time):
        self.id = id
        self.day = day
        self.time = time
        
    def __str__(self):
        return f"{self.day} {self.time}"
