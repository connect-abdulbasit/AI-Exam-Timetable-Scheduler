from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLineEdit, QSpinBox, QComboBox, QFormLayout,
                             QGroupBox, QLabel, QTableWidget, QTableWidgetItem,
                             QHeaderView, QStyle, QMessageBox, QFileDialog)
from PyQt5.QtCore import Qt
from ..models import Course, Room, TimeSlot

class ConfigTab(QWidget):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.init_ui()

    def init_ui(self):
        tab_main_layout = QVBoxLayout(self)

        header_widget = QWidget()
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(10, 10, 10, 10)

        load_btn = QPushButton("Load Configuration")
        load_btn.setObjectName("primaryAction")
        load_btn.clicked.connect(self.load_config_file)

        save_btn = QPushButton("Save Configuration")
        save_btn.clicked.connect(self.save_config_file)

        load_default_btn = QPushButton("Load Defaults")
        load_default_btn.clicked.connect(self.load_default_config)

        header_layout.addWidget(load_btn)
        header_layout.addWidget(save_btn)
        header_layout.addWidget(load_default_btn)
        header_layout.addStretch()
        tab_main_layout.addWidget(header_widget)

        content_layout = QHBoxLayout()

        left_column = QVBoxLayout()

        courses_group = QGroupBox("Add New Course")
        courses_form = QFormLayout()
        self.course_id_input = QLineEdit()
        self.course_id_input.setPlaceholderText("e.g., CS101")
        self.course_name_input = QLineEdit()
        self.course_instructor_input = QLineEdit()
        self.course_students_input = QSpinBox()
        self.course_students_input.setMaximum(999)

        courses_form.addRow("Course ID:", self.course_id_input)
        courses_form.addRow("Course Name:", self.course_name_input)
        courses_form.addRow("Instructor:", self.course_instructor_input)
        courses_form.addRow("Students:", self.course_students_input)

        add_course_btn = QPushButton("Add Course")
        add_course_btn.setObjectName("primaryAction")
        add_course_btn.clicked.connect(self.add_course)
        courses_form.addRow("", add_course_btn)
        courses_group.setLayout(courses_form)
        left_column.addWidget(courses_group)

        rooms_group = QGroupBox("Add New Room")
        rooms_form = QFormLayout()
        self.room_id_input = QLineEdit()
        self.room_capacity_input = QSpinBox()
        self.room_capacity_input.setMaximum(999)

        rooms_form.addRow("Room ID:", self.room_id_input)
        rooms_form.addRow("Capacity:", self.room_capacity_input)

        add_room_btn = QPushButton("Add Room")
        add_room_btn.setObjectName("primaryAction")
        add_room_btn.clicked.connect(self.add_room)
        rooms_form.addRow("", add_room_btn)
        rooms_group.setLayout(rooms_form)
        left_column.addWidget(rooms_group)

        slots_group = QGroupBox("Add New Time Slot")
        slots_form = QFormLayout()
        self.slot_id_input = QLineEdit()
        self.slot_day_input = QComboBox()
        self.slot_day_input.addItems(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])
        self.slot_time_input = QLineEdit()
        self.slot_time_input.setPlaceholderText("e.g., 09:00 AM")

        slots_form.addRow("Slot ID:", self.slot_id_input)
        slots_form.addRow("Day:", self.slot_day_input)
        slots_form.addRow("Time:", self.slot_time_input)

        add_slot_btn = QPushButton("Add Time Slot")
        add_slot_btn.setObjectName("primaryAction")
        add_slot_btn.clicked.connect(self.add_timeslot)
        slots_form.addRow("", add_slot_btn)
        slots_group.setLayout(slots_form)
        left_column.addWidget(slots_group)

        left_column.addStretch()
        content_layout.addLayout(left_column, 1)

        right_column = QVBoxLayout()

        tables_group = QGroupBox("Current Configuration")
        tables_layout = QVBoxLayout()

        tables_layout.addWidget(QLabel("Courses:"))
        self.courses_table = QTableWidget()
        self.courses_table.setColumnCount(5)
        self.courses_table.setHorizontalHeaderLabels(["ID", "Name", "Instructor", "Students", ""])
        self.courses_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.courses_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        tables_layout.addWidget(self.courses_table)

        tables_layout.addWidget(QLabel("Rooms:"))
        self.rooms_table = QTableWidget()
        self.rooms_table.setColumnCount(3)
        self.rooms_table.setHorizontalHeaderLabels(["ID", "Capacity", ""])
        self.rooms_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.rooms_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        tables_layout.addWidget(self.rooms_table)

        tables_layout.addWidget(QLabel("Time Slots:"))
        self.slots_table = QTableWidget()
        self.slots_table.setColumnCount(4)
        self.slots_table.setHorizontalHeaderLabels(["ID", "Day", "Time", ""])
        self.slots_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.slots_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        tables_layout.addWidget(self.slots_table)

        tables_layout.addWidget(QLabel("Student Conflict Groups:"))
        self.groups_table = QTableWidget()
        self.groups_table.setColumnCount(2)
        self.groups_table.setHorizontalHeaderLabels(["Group", "Courses"])
        self.groups_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        tables_layout.addWidget(self.groups_table)

        tables_group.setLayout(tables_layout)
        right_column.addWidget(tables_group)

        content_layout.addLayout(right_column, 2)
        tab_main_layout.addLayout(content_layout)

        self.refresh_all()

    def refresh_all(self):
        self.refresh_courses_table()
        self.refresh_rooms_table()
        self.refresh_slots_table()
        self.refresh_groups_table()

    def add_course(self):
        course_id = self.course_id_input.text().strip()
        name = self.course_name_input.text().strip()
        instructor = self.course_instructor_input.text().strip()
        students = self.course_students_input.value()

        if not course_id or not name or not instructor or students == 0:
            QMessageBox.warning(self, "Input Error", "Please fill all course fields")
            return

        if any(c.id == course_id for c in self.config.courses):
            QMessageBox.warning(self, "Duplicate ID", f"Course ID '{course_id}' already exists")
            return

        self.config.courses.append(Course(course_id, name, instructor, students))
        self.refresh_courses_table()
        self.course_id_input.clear()
        self.course_name_input.clear()
        self.course_instructor_input.clear()
        self.course_students_input.setValue(0)

    def add_room(self):
        room_id = self.room_id_input.text().strip()
        capacity = self.room_capacity_input.value()
        if not room_id or capacity == 0:
            QMessageBox.warning(self, "Input Error", "Please fill all room fields")
            return
        if any(r.id == room_id for r in self.config.rooms):
            QMessageBox.warning(self, "Duplicate ID", f"Room ID '{room_id}' already exists")
            return
        self.config.rooms.append(Room(room_id, capacity))
        self.refresh_rooms_table()
        self.room_id_input.clear()
        self.room_capacity_input.setValue(0)

    def add_timeslot(self):
        slot_id = self.slot_id_input.text().strip()
        day = self.slot_day_input.currentText()
        time = self.slot_time_input.text().strip()
        if not slot_id or not time:
            QMessageBox.warning(self, "Input Error", "Please fill all time slot fields")
            return
        if any(t.id == slot_id for t in self.config.timeslots):
            QMessageBox.warning(self, "Duplicate ID", f"Slot ID '{slot_id}' already exists")
            return
        self.config.timeslots.append(TimeSlot(slot_id, day, time))
        self.refresh_slots_table()
        self.slot_id_input.clear()
        self.slot_time_input.clear()

    def refresh_courses_table(self):
        self.courses_table.setRowCount(len(self.config.courses))
        for i, course in enumerate(self.config.courses):
            self.courses_table.setItem(i, 0, QTableWidgetItem(course.id))
            self.courses_table.setItem(i, 1, QTableWidgetItem(course.name))
            self.courses_table.setItem(i, 2, QTableWidgetItem(course.instructor))
            self.courses_table.setItem(i, 3, QTableWidgetItem(str(course.students_enrolled)))

            remove_btn = QPushButton()
            remove_btn.setIcon(self.style().standardIcon(QStyle.SP_TrashIcon))
            remove_btn.setObjectName("dangerAction")
            remove_btn.setToolTip("Remove Course")
            remove_btn.setFixedWidth(40)
            remove_btn.clicked.connect(lambda checked, row=i: self.remove_course(row))
            self.courses_table.setCellWidget(i, 4, remove_btn)

    def refresh_rooms_table(self):
        self.rooms_table.setRowCount(len(self.config.rooms))
        for i, room in enumerate(self.config.rooms):
            self.rooms_table.setItem(i, 0, QTableWidgetItem(room.id))
            self.rooms_table.setItem(i, 1, QTableWidgetItem(str(room.capacity)))
            remove_btn = QPushButton()
            remove_btn.setIcon(self.style().standardIcon(QStyle.SP_TrashIcon))
            remove_btn.setObjectName("dangerAction")
            remove_btn.setToolTip("Remove Room")
            remove_btn.setFixedWidth(40)
            remove_btn.clicked.connect(lambda checked, row=i: self.remove_room(row))
            self.rooms_table.setCellWidget(i, 2, remove_btn)

    def refresh_slots_table(self):
        self.slots_table.setRowCount(len(self.config.timeslots))
        for i, slot in enumerate(self.config.timeslots):
            self.slots_table.setItem(i, 0, QTableWidgetItem(slot.id))
            self.slots_table.setItem(i, 1, QTableWidgetItem(slot.day))
            self.slots_table.setItem(i, 2, QTableWidgetItem(slot.time))
            remove_btn = QPushButton()
            remove_btn.setIcon(self.style().standardIcon(QStyle.SP_TrashIcon))
            remove_btn.setObjectName("dangerAction")
            remove_btn.setToolTip("Remove Time Slot")
            remove_btn.setFixedWidth(40)
            remove_btn.clicked.connect(lambda checked, row=i: self.remove_timeslot(row))
            self.slots_table.setCellWidget(i, 3, remove_btn)
        self.refresh_groups_table()

    def refresh_groups_table(self):
        self.groups_table.setRowCount(len(self.config.student_conflict_groups))
        for i, group in enumerate(self.config.student_conflict_groups):
            self.groups_table.setItem(i, 0, QTableWidgetItem(f"Group {i+1}"))
            self.groups_table.setItem(i, 1, QTableWidgetItem(", ".join(group)))

    def remove_course(self, row):
        if 0 <= row < len(self.config.courses):
            self.config.courses.pop(row)
            self.refresh_courses_table()

    def remove_room(self, row):
        if 0 <= row < len(self.config.rooms):
            self.config.rooms.pop(row)
            self.refresh_rooms_table()

    def remove_timeslot(self, row):
        if 0 <= row < len(self.config.timeslots):
            self.config.timeslots.pop(row)
            self.refresh_slots_table()

    def load_config_file(self):
        filepath, _ = QFileDialog.getOpenFileName(self, "Load Configuration", "", "JSON Files (*.json)")
        if filepath:
            success, message = self.config.load_from_file(filepath)
            QMessageBox.information(self, "Load Configuration", message)
            if success:
                self.refresh_all()

    def save_config_file(self):
        filepath, _ = QFileDialog.getSaveFileName(self, "Save Configuration", "config.json", "JSON Files (*.json)")
        if filepath:
            self.config.save_to_file(filepath)
            QMessageBox.information(self, "Save Configuration", f"Configuration saved to {filepath}")

    def load_default_config(self):
        self.config.load_defaults()
        self.refresh_all()
        QMessageBox.information(self, "Load Defaults", "Default configuration loaded")
