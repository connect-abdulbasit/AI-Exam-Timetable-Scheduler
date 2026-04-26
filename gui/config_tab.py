from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLineEdit, QSpinBox, QComboBox, QFormLayout,
                             QGroupBox, QLabel, QTableWidget, QTableWidgetItem,
                             QHeaderView, QStyle, QMessageBox, QFileDialog,
                             QScrollArea, QSplitter, QFrame, QSizePolicy)
from PyQt5.QtCore import Qt
from ..models import Course, Room, TimeSlot


class ConfigTab(QWidget):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.init_ui()

    def _wrap_scroll(self, inner: QWidget) -> QScrollArea:
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(inner)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        return scroll

    def init_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(20, 16, 20, 16)
        root.setSpacing(14)

        title = QLabel("Exam data")
        title.setObjectName("pageTitle")
        subtitle = QLabel(
            "The app starts with no exam data. Load a JSON file below (or add rows manually). "
            "The tables on the right show exactly what Run will use."
        )
        subtitle.setObjectName("pageSubtitle")
        subtitle.setWordWrap(True)
        root.addWidget(title)
        root.addWidget(subtitle)

        self.data_status = QLabel()
        self.data_status.setObjectName("dataStatusBanner")
        self.data_status.setWordWrap(True)
        root.addWidget(self.data_status)

        strip = QFrame()
        strip.setObjectName("infoStrip")
        strip_layout = QVBoxLayout(strip)
        strip_layout.setContentsMargins(0, 0, 0, 0)
        strip_text = QLabel(
            "<b>Workflow</b> — Nothing loads automatically. Use <b>Load JSON…</b> and pick your file "
            "(same shape as <code>data/exam_config.json</code>), or add rows manually. "
            "Optional: <code>data/exam_config_unsatisfiable.json</code> is built so cohort rules cannot all be satisfied "
            "(fewer slots than courses in one group) — runs should finish with fitness below 1.0. "
            "Keys: <code>courses</code>, <code>rooms</code>, <code>timeslots</code>, <code>student_conflicts</code>."
        )
        strip_text.setObjectName("infoStripText")
        strip_text.setWordWrap(True)
        strip_text.setTextFormat(Qt.RichText)
        strip_layout.addWidget(strip_text)
        root.addWidget(strip)

        toolbar = QHBoxLayout()
        toolbar.setSpacing(10)
        load_btn = QPushButton("Load JSON…")
        load_btn.setObjectName("primaryAction")
        load_btn.setToolTip("Replace current data from your exam configuration JSON")
        load_btn.clicked.connect(self.load_config_file)

        save_btn = QPushButton("Save JSON…")
        save_btn.setToolTip("Write courses, rooms, time slots, and conflict groups to disk")
        save_btn.clicked.connect(self.save_config_file)

        toolbar.addWidget(load_btn)
        toolbar.addWidget(save_btn)
        toolbar.addStretch()
        root.addLayout(toolbar)

        splitter = QSplitter(Qt.Horizontal)
        splitter.setChildrenCollapsible(False)

        left_inner = QWidget()
        left_col = QVBoxLayout(left_inner)
        left_col.setSpacing(16)
        left_col.setContentsMargins(0, 0, 12, 0)

        courses_group = QGroupBox("Courses")
        courses_hint = QLabel("Exams to schedule — each needs a unique ID.")
        courses_hint.setObjectName("sectionHint")
        courses_hint.setWordWrap(True)
        courses_form = QFormLayout()
        self.course_id_input = QLineEdit()
        self.course_id_input.setPlaceholderText("e.g. CS101")
        self.course_name_input = QLineEdit()
        self.course_instructor_input = QLineEdit()
        self.course_students_input = QSpinBox()
        self.course_students_input.setMaximum(999)

        courses_form.addRow("Course ID:", self.course_id_input)
        courses_form.addRow("Title:", self.course_name_input)
        courses_form.addRow("Instructor:", self.course_instructor_input)
        courses_form.addRow("Students enrolled:", self.course_students_input)

        add_course_btn = QPushButton("Add to list")
        add_course_btn.setObjectName("primaryAction")
        add_course_btn.clicked.connect(self.add_course)
        courses_form.addRow("", add_course_btn)
        cg_layout = QVBoxLayout()
        cg_layout.addWidget(courses_hint)
        cg_layout.addLayout(courses_form)
        courses_group.setLayout(cg_layout)
        left_col.addWidget(courses_group)

        rooms_group = QGroupBox("Rooms")
        rooms_hint = QLabel("Rooms must fit peak enrollment for any exam placed there.")
        rooms_hint.setObjectName("sectionHint")
        rooms_hint.setWordWrap(True)
        rooms_form = QFormLayout()
        self.room_id_input = QLineEdit()
        self.room_id_input.setPlaceholderText("e.g. Hall A")
        self.room_capacity_input = QSpinBox()
        self.room_capacity_input.setMaximum(999)

        rooms_form.addRow("Room ID:", self.room_id_input)
        rooms_form.addRow("Seat capacity:", self.room_capacity_input)

        add_room_btn = QPushButton("Add to list")
        add_room_btn.setObjectName("primaryAction")
        add_room_btn.clicked.connect(self.add_room)
        rooms_form.addRow("", add_room_btn)
        rg_layout = QVBoxLayout()
        rg_layout.addWidget(rooms_hint)
        rg_layout.addLayout(rooms_form)
        rooms_group.setLayout(rg_layout)
        left_col.addWidget(rooms_group)

        slots_group = QGroupBox("Time slots")
        slots_hint = QLabel("Each slot is one possible exam window (day + time label).")
        slots_hint.setObjectName("sectionHint")
        slots_hint.setWordWrap(True)
        slots_form = QFormLayout()
        self.slot_id_input = QLineEdit()
        self.slot_id_input.setPlaceholderText("e.g. T1")
        self.slot_day_input = QComboBox()
        self.slot_day_input.addItems(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])
        self.slot_time_input = QLineEdit()
        self.slot_time_input.setPlaceholderText("e.g. 09:00 AM")

        slots_form.addRow("Slot ID:", self.slot_id_input)
        slots_form.addRow("Day:", self.slot_day_input)
        slots_form.addRow("Time label:", self.slot_time_input)

        add_slot_btn = QPushButton("Add to list")
        add_slot_btn.setObjectName("primaryAction")
        add_slot_btn.clicked.connect(self.add_timeslot)
        slots_form.addRow("", add_slot_btn)
        sg_layout = QVBoxLayout()
        sg_layout.addWidget(slots_hint)
        sg_layout.addLayout(slots_form)
        slots_group.setLayout(sg_layout)
        left_col.addWidget(slots_group)

        left_col.addStretch()
        left_scroll = self._wrap_scroll(left_inner)
        left_scroll.setMinimumWidth(340)
        splitter.addWidget(left_scroll)

        right_inner = QWidget()
        right_col = QVBoxLayout(right_inner)
        right_col.setSpacing(0)
        right_col.setContentsMargins(12, 0, 0, 0)

        preview = QGroupBox("Live preview — what Run will use")
        tables_layout = QVBoxLayout()
        tables_layout.setSpacing(6)

        def section(title: str) -> QLabel:
            lab = QLabel(title)
            lab.setObjectName("tableSectionTitle")
            return lab

        tables_layout.addWidget(section("Courses"))
        self.courses_table = QTableWidget()
        self.courses_table.setColumnCount(5)
        self.courses_table.setHorizontalHeaderLabels(["ID", "Name", "Instructor", "Students", ""])
        self.courses_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.courses_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.courses_table.setMinimumHeight(130)
        self.courses_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        tables_layout.addWidget(self.courses_table)

        tables_layout.addWidget(section("Rooms"))
        self.rooms_table = QTableWidget()
        self.rooms_table.setColumnCount(3)
        self.rooms_table.setHorizontalHeaderLabels(["ID", "Capacity", ""])
        self.rooms_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.rooms_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.rooms_table.setMinimumHeight(100)
        tables_layout.addWidget(self.rooms_table)

        tables_layout.addWidget(section("Time slots"))
        self.slots_table = QTableWidget()
        self.slots_table.setColumnCount(4)
        self.slots_table.setHorizontalHeaderLabels(["ID", "Day", "Time", ""])
        self.slots_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.slots_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.slots_table.setMinimumHeight(100)
        tables_layout.addWidget(self.slots_table)

        tables_layout.addWidget(section("Student conflict groups (read-only)"))
        groups_expl = QLabel(
            "Courses in the same group must not overlap for students. "
            "Edit groups by loading a JSON file that includes \"student_conflicts\"."
        )
        groups_expl.setObjectName("sectionHint")
        groups_expl.setWordWrap(True)
        tables_layout.addWidget(groups_expl)
        self.groups_table = QTableWidget()
        self.groups_table.setColumnCount(2)
        self.groups_table.setHorizontalHeaderLabels(["Group", "Courses"])
        self.groups_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.groups_table.setMinimumHeight(80)
        tables_layout.addWidget(self.groups_table)

        preview.setLayout(tables_layout)
        right_col.addWidget(preview)

        right_scroll = self._wrap_scroll(right_inner)
        splitter.addWidget(right_scroll)
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        splitter.setSizes([400, 700])

        root.addWidget(splitter, 1)

        self.refresh_all()

    def _update_data_status_banner(self):
        errs = self.config.validate()
        warn = bool(errs)
        self.data_status.setProperty("warning", warn)
        self.data_status.style().unpolish(self.data_status)
        self.data_status.style().polish(self.data_status)
        if errs:
            self.data_status.setText(
                "Still missing: " + " · ".join(errs)
                + " — use Load JSON… or add rows below."
            )
        else:
            src = self.config.loaded_from_path or "in-memory only (save JSON to keep a path on disk)"
            self.data_status.setText(f"Configuration is valid. Active data: {src}")

    def refresh_all(self):
        self.refresh_courses_table()
        self.refresh_rooms_table()
        self.refresh_slots_table()
        self.refresh_groups_table()
        self._update_data_status_banner()

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
        self._update_data_status_banner()
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
        self._update_data_status_banner()
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
        self._update_data_status_banner()
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
            self._update_data_status_banner()

    def remove_room(self, row):
        if 0 <= row < len(self.config.rooms):
            self.config.rooms.pop(row)
            self.refresh_rooms_table()
            self._update_data_status_banner()

    def remove_timeslot(self, row):
        if 0 <= row < len(self.config.timeslots):
            self.config.timeslots.pop(row)
            self.refresh_slots_table()
            self._update_data_status_banner()

    def load_config_file(self):
        filepath, _ = QFileDialog.getOpenFileName(
            self,
            "Load exam configuration",
            "",
            "JSON Files (*.json);;All Files (*)",
        )
        if filepath:
            success, message = self.config.load_from_file(filepath)
            if success:
                self.refresh_all()
                QMessageBox.information(self, "Load configuration", message)
            else:
                QMessageBox.warning(self, "Load configuration", message)
                self._update_data_status_banner()

    def save_config_file(self):
        filepath, _ = QFileDialog.getSaveFileName(
            self,
            "Save exam configuration",
            "exam_config.json",
            "JSON Files (*.json);;All Files (*)",
        )
        if filepath:
            self.config.save_to_file(filepath)
            self._update_data_status_banner()
            QMessageBox.information(self, "Save configuration", f"Saved to:\n{filepath}")
