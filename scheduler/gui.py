import sys
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                             QPushButton, QTextEdit, QLabel, QTabWidget, QTableWidget, 
                             QTableWidgetItem, QHeaderView, QProgressBar, QHBoxLayout,
                             QLineEdit, QSpinBox, QComboBox, QFormLayout,
                             QGroupBox, QMessageBox, QFileDialog,
                             QScrollArea)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from .models import Course, Room, TimeSlot
from .config import Configuration
from .worker import GAWorker

class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Exam Timetable Scheduler Pro")
        self.setGeometry(100, 100, 1100, 800)

        # Initialize configuration
        self.config = Configuration()

        # Tab Widget
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Initialize Tabs
        self.init_config_tab()
        self.init_control_tab()
        self.init_graph_tab()
        self.init_results_tab()

        self.gen_data = []
        self.fitness_data = []

    def init_config_tab(self):
        """Configuration input tab"""
        tab = QWidget()
        tab_main_layout = QVBoxLayout(tab)
        
        # Scroll Area for configuration
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        layout = QVBoxLayout(scroll_content)

        # File operations
        file_layout = QHBoxLayout()
        load_btn = QPushButton("Load Configuration")
        load_btn.clicked.connect(self.load_config_file)
        save_btn = QPushButton("Save Configuration")
        save_btn.clicked.connect(self.save_config_file)
        load_default_btn = QPushButton("Load Defaults")
        load_default_btn.clicked.connect(self.load_default_config)
        file_layout.addWidget(load_btn)
        file_layout.addWidget(save_btn)
        file_layout.addWidget(load_default_btn)
        file_layout.addStretch()
        layout.addLayout(file_layout)

        # Courses section
        courses_group = QGroupBox("Courses")
        courses_layout = QVBoxLayout()
        
        courses_form = QFormLayout()
        self.course_id_input = QLineEdit()
        self.course_name_input = QLineEdit()
        self.course_instructor_input = QLineEdit()
        self.course_students_input = QSpinBox()
        self.course_students_input.setMaximum(999)
        
        courses_form.addRow("Course ID:", self.course_id_input)
        courses_form.addRow("Course Name:", self.course_name_input)
        courses_form.addRow("Instructor:", self.course_instructor_input)
        courses_form.addRow("Students Enrolled:", self.course_students_input)
        
        add_course_btn = QPushButton("Add Course")
        add_course_btn.clicked.connect(self.add_course)
        courses_form.addRow("", add_course_btn)
        
        courses_layout.addLayout(courses_form)
        
        self.courses_table = QTableWidget()
        self.courses_table.setColumnCount(5)
        self.courses_table.setHorizontalHeaderLabels(["ID", "Name", "Instructor", "Students", "Remove"])
        self.courses_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.courses_table.setMaximumHeight(150)
        courses_layout.addWidget(self.courses_table)
        
        courses_group.setLayout(courses_layout)
        layout.addWidget(courses_group)

        # Rooms section
        rooms_group = QGroupBox("Rooms")
        rooms_layout = QVBoxLayout()
        
        rooms_form = QFormLayout()
        self.room_id_input = QLineEdit()
        self.room_capacity_input = QSpinBox()
        self.room_capacity_input.setMaximum(999)
        
        rooms_form.addRow("Room ID:", self.room_id_input)
        rooms_form.addRow("Capacity:", self.room_capacity_input)
        
        add_room_btn = QPushButton("Add Room")
        add_room_btn.clicked.connect(self.add_room)
        rooms_form.addRow("", add_room_btn)
        
        rooms_layout.addLayout(rooms_form)
        
        self.rooms_table = QTableWidget()
        self.rooms_table.setColumnCount(3)
        self.rooms_table.setHorizontalHeaderLabels(["ID", "Capacity", "Remove"])
        self.rooms_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.rooms_table.setMaximumHeight(120)
        rooms_layout.addWidget(self.rooms_table)
        
        rooms_group.setLayout(rooms_layout)
        layout.addWidget(rooms_group)

        # Time Slots section
        slots_group = QGroupBox("Time Slots")
        slots_layout = QVBoxLayout()
        
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
        add_slot_btn.clicked.connect(self.add_timeslot)
        slots_form.addRow("", add_slot_btn)
        
        slots_layout.addLayout(slots_form)
        
        self.slots_table = QTableWidget()
        self.slots_table.setColumnCount(4)
        self.slots_table.setHorizontalHeaderLabels(["ID", "Day", "Time", "Remove"])
        self.slots_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.slots_table.setMaximumHeight(120)
        slots_layout.addWidget(self.slots_table)
        
        slots_group.setLayout(slots_layout)
        layout.addWidget(slots_group)

        layout.addStretch()
        scroll.setWidget(scroll_content)
        tab_main_layout.addWidget(scroll)
        self.tabs.addTab(tab, "Configuration")

    def add_course(self):
        """Add course to configuration"""
        course_id = self.course_id_input.text().strip()
        name = self.course_name_input.text().strip()
        instructor = self.course_instructor_input.text().strip()
        students = self.course_students_input.value()
        
        if not course_id or not name or not instructor or students == 0:
            QMessageBox.warning(self, "Input Error", "Please fill all course fields")
            return
        
        # Check for duplicate ID
        if any(c.id == course_id for c in self.config.courses):
            QMessageBox.warning(self, "Duplicate ID", f"Course ID '{course_id}' already exists")
            return
        
        self.config.courses.append(Course(course_id, name, instructor, students))
        self.refresh_courses_table()
        
        # Clear inputs
        self.course_id_input.clear()
        self.course_name_input.clear()
        self.course_instructor_input.clear()
        self.course_students_input.setValue(0)

    def add_room(self):
        """Add room to configuration"""
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
        """Add time slot to configuration"""
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
        """Refresh the courses table display"""
        self.courses_table.setRowCount(len(self.config.courses))
        for i, course in enumerate(self.config.courses):
            self.courses_table.setItem(i, 0, QTableWidgetItem(course.id))
            self.courses_table.setItem(i, 1, QTableWidgetItem(course.name))
            self.courses_table.setItem(i, 2, QTableWidgetItem(course.instructor))
            self.courses_table.setItem(i, 3, QTableWidgetItem(str(course.students_enrolled)))
            
            remove_btn = QPushButton("Remove")
            remove_btn.clicked.connect(lambda checked, row=i: self.remove_course(row))
            self.courses_table.setCellWidget(i, 4, remove_btn)

    def refresh_rooms_table(self):
        """Refresh the rooms table display"""
        self.rooms_table.setRowCount(len(self.config.rooms))
        for i, room in enumerate(self.config.rooms):
            self.rooms_table.setItem(i, 0, QTableWidgetItem(room.id))
            self.rooms_table.setItem(i, 1, QTableWidgetItem(str(room.capacity)))
            
            remove_btn = QPushButton("Remove")
            remove_btn.clicked.connect(lambda checked, row=i: self.remove_room(row))
            self.rooms_table.setCellWidget(i, 2, remove_btn)

    def refresh_slots_table(self):
        """Refresh the time slots table display"""
        self.slots_table.setRowCount(len(self.config.timeslots))
        for i, slot in enumerate(self.config.timeslots):
            self.slots_table.setItem(i, 0, QTableWidgetItem(slot.id))
            self.slots_table.setItem(i, 1, QTableWidgetItem(slot.day))
            self.slots_table.setItem(i, 2, QTableWidgetItem(slot.time))
            
            remove_btn = QPushButton("Remove")
            remove_btn.clicked.connect(lambda checked, row=i: self.remove_timeslot(row))
            self.slots_table.setCellWidget(i, 3, remove_btn)

    def remove_course(self, row):
        """Remove course from configuration"""
        if 0 <= row < len(self.config.courses):
            self.config.courses.pop(row)
            self.refresh_courses_table()

    def remove_room(self, row):
        """Remove room from configuration"""
        if 0 <= row < len(self.config.rooms):
            self.config.rooms.pop(row)
            self.refresh_rooms_table()

    def remove_timeslot(self, row):
        """Remove time slot from configuration"""
        if 0 <= row < len(self.config.timeslots):
            self.config.timeslots.pop(row)
            self.refresh_slots_table()

    def load_config_file(self):
        """Load configuration from file"""
        filepath, _ = QFileDialog.getOpenFileName(self, "Load Configuration", "", "JSON Files (*.json)")
        if filepath:
            success, message = self.config.load_from_file(filepath)
            QMessageBox.information(self, "Load Configuration", message)
            if success:
                self.refresh_courses_table()
                self.refresh_rooms_table()
                self.refresh_slots_table()

    def save_config_file(self):
        """Save configuration to file"""
        filepath, _ = QFileDialog.getSaveFileName(self, "Save Configuration", "config.json", "JSON Files (*.json)")
        if filepath:
            self.config.save_to_file(filepath)
            QMessageBox.information(self, "Save Configuration", f"Configuration saved to {filepath}")

    def load_default_config(self):
        """Load default configuration"""
        self.config.load_defaults()
        self.refresh_courses_table()
        self.refresh_rooms_table()
        self.refresh_slots_table()
        QMessageBox.information(self, "Load Defaults", "Default configuration loaded")

    def init_control_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        self.status_label = QLabel("Status: Idle. Ready to generate schedule.")
        self.status_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        layout.addWidget(self.status_label)

        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(200) # Max generations
        layout.addWidget(self.progress_bar)

        self.start_btn = QPushButton("Run Genetic Algorithm")
        self.start_btn.setMinimumHeight(50)
        self.start_btn.setStyleSheet("font-size: 14px; font-weight: bold; background-color: #2b5797; color: white;")
        self.start_btn.clicked.connect(self.start_ga)
        layout.addWidget(self.start_btn)

        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        layout.addWidget(QLabel("Live Generation Logs:"))
        layout.addWidget(self.log_output)

        tab.setLayout(layout)
        self.tabs.addTab(tab, "Control Panel")

    def init_graph_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_title("Evolution Tracking: Fitness over Generations")
        self.ax.set_xlabel("Generation")
        self.ax.set_ylabel("Fitness Score (1.0 = Perfect)")
        self.ax.grid(True)
        
        layout.addWidget(self.canvas)
        tab.setLayout(layout)
        self.tabs.addTab(tab, "Live Visualization")

    def init_results_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Course ID", "Course Name", "Instructor", "Room", "Time Slot"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)

        tab.setLayout(layout)
        self.tabs.addTab(tab, "Optimized Timetable")

    def start_ga(self):
        # Validate configuration
        errors = self.config.validate()
        if errors:
            QMessageBox.warning(self, "Configuration Error", "Issues:\n" + "\n".join(errors))
            return
        
        self.start_btn.setEnabled(False)
        self.log_output.clear()
        self.gen_data.clear()
        self.fitness_data.clear()
        self.ax.clear()
        self.table.setRowCount(0)
        
        # Setup graph baseline
        self.ax.set_title("Evolution Tracking: Fitness over Generations")
        self.ax.set_xlabel("Generation")
        self.ax.set_ylabel("Fitness Score (1.0 = Perfect)")
        self.ax.grid(True)
        self.line, = self.ax.plot([], [], 'b-', linewidth=2)

        self.worker = GAWorker(self.config)
        self.worker.progress_update.connect(self.update_progress)
        self.worker.finished_signal.connect(self.ga_finished)
        self.worker.start()

    def update_progress(self, gen, fitness, current_best):
        self.status_label.setText(f"Status: Evolving... Generation {gen}")
        self.progress_bar.setValue(gen)
        self.log_output.append(f"Gen {gen:03d} | Best Fitness: {fitness:.4f}")

        # Update Graph
        self.gen_data.append(gen)
        self.fitness_data.append(fitness)
        self.line.set_data(self.gen_data, self.fitness_data)
        self.ax.relim()
        self.ax.autoscale_view()
        self.canvas.draw()

    def ga_finished(self, final_timetable, final_fitness):
        self.progress_bar.setValue(200)
        self.start_btn.setEnabled(True)
        
        if final_fitness == 1.0:
            self.status_label.setText("Status: SUCCESS! Conflict-free timetable found.")
            self.status_label.setStyleSheet("font-size: 14px; font-weight: bold; color: green;")
        else:
            self.status_label.setText("Status: Optimization finished with minor conflicts.")
            self.status_label.setStyleSheet("font-size: 14px; font-weight: bold; color: orange;")

        self.populate_table(final_timetable)
        self.tabs.setCurrentIndex(3) # Auto-switch to results tab

    def populate_table(self, timetable):
        self.table.setRowCount(len(timetable))
        course_map = {c.id: c for c in self.config.courses}
        room_map = {r.id: r for r in self.config.rooms}
        time_map = {t.id: t for t in self.config.timeslots}

        row = 0
        for course_id, (room_id, timeslot_id) in timetable.items():
            course = course_map[course_id]
            room = room_map[room_id]
            ts = time_map[timeslot_id]

            self.table.setItem(row, 0, QTableWidgetItem(course.id))
            self.table.setItem(row, 1, QTableWidgetItem(course.name))
            self.table.setItem(row, 2, QTableWidgetItem(course.instructor))
            self.table.setItem(row, 3, QTableWidgetItem(f"{room.id} (Cap: {room.capacity})"))
            self.table.setItem(row, 4, QTableWidgetItem(str(ts)))
            row += 1
