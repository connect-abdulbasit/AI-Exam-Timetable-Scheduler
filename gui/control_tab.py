from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QProgressBar, QTextEdit, QGroupBox)
from PyQt5.QtCore import Qt

class ControlTab(QWidget):
    def __init__(self, run_ga_callback):
        super().__init__()
        self.run_ga_callback = run_ga_callback
        self.init_ui()

    _STATUS_IDLE_STYLE = "font-size: 18px; font-weight: bold; color: #4fc1ff; margin-bottom: 10px;"

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 28, 32, 28)
        layout.setSpacing(18)

        status_group = QGroupBox("Run status")
        status_layout = QVBoxLayout()
        self.status_label = QLabel("Ready — not running")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet(self._STATUS_IDLE_STYLE)
        status_layout.addWidget(self.status_label)
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(200)
        self.progress_bar.setFormat("Generation %v / %m")
        status_layout.addWidget(self.progress_bar)
        status_group.setLayout(status_layout)
        layout.addWidget(status_group)
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        self.start_btn = QPushButton("Run genetic algorithm")
        self.start_btn.setObjectName("primaryAction")
        self.start_btn.setMinimumHeight(52)
        self.start_btn.setMinimumWidth(280)
        self.start_btn.clicked.connect(self.run_ga_callback)
        btn_layout.addWidget(self.start_btn)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        log_group = QGroupBox("Run log")
        log_layout = QVBoxLayout()
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setPlaceholderText("Log lines appear here when you start a run…")
        log_layout.addWidget(self.log_output)
        log_group.setLayout(log_layout)
        layout.addWidget(log_group)

    def update_status(self, text, style=None):
        self.status_label.setText(text)
        if style:
            self.status_label.setStyleSheet(style)
        else:
            self.status_label.setStyleSheet(self._STATUS_IDLE_STYLE)

    def update_progress(self, val):
        self.progress_bar.setValue(val)

    def log(self, message):
        self.log_output.append(message)

    def clear_logs(self):
        self.log_output.clear()

    def set_running(self, running):
        self.start_btn.setEnabled(not running)
