from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtGui import QColor

class ResultsTab(QWidget):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Course ID", "Course Name", "Instructor", "Room", "Time Slot", "Student Group"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setAlternatingRowColors(True)
        self.table.setShowGrid(False)
        self.table.verticalHeader().setVisible(False)
        layout.addWidget(self.table)

    def populate(self, timetable):
        self.table.setRowCount(len(timetable))
        course_map = {c.id: c for c in self.config.courses}
        room_map = {r.id: r for r in self.config.rooms}
        time_map = {t.id: t for t in self.config.timeslots}
        GROUP_COLORS = [
            QColor("#1a3a5a"), 
            QColor("#1e4620"), 
            QColor("#5a4b1e"), 
            QColor("#4b2e5a"), 
            QColor("#5a2e2e"), 
            QColor("#2e5a5a"), 
        ]
        row = 0
        for course_id, (room_id, timeslot_id) in timetable.items():
            course = course_map[course_id]
            room = room_map[room_id]
            ts = time_map[timeslot_id]
            group_idx = self.config.get_course_group(course_id)
            bg_color = GROUP_COLORS[group_idx % len(GROUP_COLORS)] if group_idx != -1 else None
            items = [
                QTableWidgetItem(course.id),
                QTableWidgetItem(course.name),
                QTableWidgetItem(course.instructor),
                QTableWidgetItem(f"{room.id} (Cap: {room.capacity})"),
                QTableWidgetItem(str(ts)),
                QTableWidgetItem(f"Group {group_idx + 1}" if group_idx != -1 else "None")
            ]
            for col, item in enumerate(items):
                if bg_color:
                    item.setBackground(bg_color)
                self.table.setItem(row, col, item)
            row += 1

    def clear(self):
        self.table.setRowCount(0)
