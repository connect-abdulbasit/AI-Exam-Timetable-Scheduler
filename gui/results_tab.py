import json

from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QLabel,
    QStackedWidget,
    QPushButton,
    QFileDialog,
    QMessageBox,
    QAbstractItemView,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor


class ResultsTab(QWidget):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self._last_timetable = {}
        self._last_fitness = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(12)

        title = QLabel("Timetable (assignment)")
        title.setObjectName("pageTitle")
        layout.addWidget(title)

        self.stack = QStackedWidget()
        self.empty_page = QWidget()
        empty_layout = QVBoxLayout(self.empty_page)
        empty_layout.setAlignment(Qt.AlignCenter)
        empty_layout.setSpacing(14)

        empty_title = QLabel("No assignment to show yet")
        empty_title.setObjectName("emptyStateTitle")
        empty_title.setAlignment(Qt.AlignCenter)
        empty_layout.addWidget(empty_title)

        self.table_page = QWidget()
        table_layout = QVBoxLayout(self.table_page)
        table_layout.setSpacing(10)

        toolbar = QHBoxLayout()
        self.summary_label = QLabel()
        self.summary_label.setObjectName("assignmentSummary")
        self.summary_label.setWordWrap(True)
        export_btn = QPushButton("Export assignment JSON…")
        export_btn.clicked.connect(self._export_assignment)
        toolbar.addWidget(self.summary_label, 1)
        toolbar.addWidget(export_btn)
        table_layout.addLayout(toolbar)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(
            ["Course", "Title", "Instructor", "Room", "Slot", "Conflict group"]
        )
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setAlternatingRowColors(True)
        self.table.setShowGrid(False)
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        table_layout.addWidget(self.table)

        self.stack.addWidget(self.empty_page)
        self.stack.addWidget(self.table_page)
        layout.addWidget(self.stack, 1)
        self.stack.setCurrentIndex(0)

    def populate(self, timetable, fitness=None):
        self._last_fitness = fitness
        self._last_timetable = dict(timetable) if timetable else {}
        if not timetable:
            self.clear()
            return
        self.stack.setCurrentIndex(1)
        fit_txt = f"{fitness:.4f}" if fitness is not None else "—"
        self.summary_label.setTextFormat(Qt.RichText)
        self.summary_label.setText(
            f"Best run fitness: <b>{fit_txt}</b> (1.0 = no detected conflicts). "
            f"{len(timetable)} course(s) assigned."
        )

        self.table.setRowCount(len(timetable))
        course_map = {c.id: c for c in self.config.courses}
        room_map = {r.id: r for r in self.config.rooms}
        time_map = {t.id: t for t in self.config.timeslots}
        group_colors = [
            QColor("#1a3a5a"),
            QColor("#1e4620"),
            QColor("#5a4b1e"),
            QColor("#4b2e5a"),
            QColor("#5a2e2e"),
            QColor("#2e5a5a"),
        ]
        row = 0
        for course_id, (room_id, timeslot_id) in sorted(timetable.items()):
            course = course_map.get(course_id)
            room = room_map.get(room_id)
            ts = time_map.get(timeslot_id)
            if not course or not room or not ts:
                continue
            group_idx = self.config.get_course_group(course_id)
            bg_color = group_colors[group_idx % len(group_colors)] if group_idx != -1 else None
            slot_label = f"{ts.day} · {ts.time} ({ts.id})"
            items = [
                QTableWidgetItem(course.id),
                QTableWidgetItem(course.name),
                QTableWidgetItem(course.instructor),
                QTableWidgetItem(f"{room.id}  (cap {room.capacity})"),
                QTableWidgetItem(slot_label),
                QTableWidgetItem(f"Group {group_idx + 1}" if group_idx != -1 else "—"),
            ]
            for col, item in enumerate(items):
                if bg_color:
                    item.setBackground(bg_color)
                self.table.setItem(row, col, item)
            row += 1
        self.table.setRowCount(row)

    def clear(self):
        self._last_timetable = {}
        self._last_fitness = None
        self.summary_label.clear()
        self.table.setRowCount(0)
        self.stack.setCurrentIndex(0)

    def _export_assignment(self):
        if not self._last_timetable:
            QMessageBox.information(self, "Export", "Run the scheduler first; there is no assignment to export.")
            return
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Export timetable assignment",
            "timetable_assignment.json",
            "JSON (*.json);;All files (*)",
        )
        if not path:
            return
        payload = {
            "fitness": self._last_fitness,
            "assignments": [
                {"course_id": k, "room_id": v[0], "timeslot_id": v[1]}
                for k, v in sorted(self._last_timetable.items())
            ],
        }
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(payload, f, indent=2)
            QMessageBox.information(self, "Export", f"Assignment saved to:\n{path}")
        except OSError as e:
            QMessageBox.warning(self, "Export", str(e))
