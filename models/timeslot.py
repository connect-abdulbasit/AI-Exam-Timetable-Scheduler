class TimeSlot:
    def __init__(self, id, day, time):
        self.id = id
        self.day = day
        self.time = time

    def __str__(self):
        return f"{self.day} {self.time}"
