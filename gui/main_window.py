from PyQt5.QtWidgets import QMainWindow, QTabWidget, QMessageBox, QStatusBar
from .config_tab import ConfigTab
from .control_tab import ControlTab
from .graph_tab import GraphTab
from .results_tab import ResultsTab
from .styles import DARK_STYLESHEET
from ..core.config import Configuration
from ..core.genetic_algorithm import GAWorker

class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Exam Timetable Scheduler Pro")
        self.setGeometry(100, 100, 1280, 880)
        self.setMinimumSize(980, 700)
        self.setStyleSheet(DARK_STYLESHEET)
        self.config = Configuration()
        self.gen_data = []
        self.fitness_data = []
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        self.config_tab = ConfigTab(self.config)
        self.control_tab = ControlTab(self.start_ga)
        self.graph_tab = GraphTab()
        self.results_tab = ResultsTab(self.config)
        self.tabs.addTab(self.config_tab, "1  Setup")
        self.tabs.setTabToolTip(0, "Define courses, rooms, time slots, and load or save JSON.")
        self.tabs.addTab(self.control_tab, "2  Run")
        self.tabs.setTabToolTip(1, "Start the genetic algorithm and read the run log.")
        self.tabs.addTab(self.graph_tab, "3  Chart")
        self.tabs.setTabToolTip(2, "Fitness vs generation — updates while a run is active.")
        self.tabs.addTab(self.results_tab, "4  Timetable")
        self.tabs.setTabToolTip(3, "Best schedule after each completed run.")

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.tabs.currentChanged.connect(self._on_tab_changed)
        self._on_tab_changed(self.tabs.currentIndex())

    def start_ga(self):
        errors = self.config.validate()
        if errors:
            QMessageBox.warning(self, "Configuration Error", "Issues:\n" + "\n".join(errors))
            return
        self.control_tab.set_running(True)
        self.control_tab.update_status("Starting run…")
        self.control_tab.clear_logs()
        self.gen_data.clear()
        self.fitness_data.clear()
        self.graph_tab.clear()
        self.results_tab.clear()
        self.worker = GAWorker(self.config)
        self.worker.progress_update.connect(self.update_progress)
        self.worker.finished_signal.connect(self.ga_finished)
        self.worker.start()

    def _on_tab_changed(self, index):
        tips = (
            "Tip: Load a JSON file on Setup (or add rows), then switch to Run.",
            "Tip: Run uses the data from Setup. Validation errors open in a dialog.",
            "Tip: This chart fills as generations complete — stay on Run to drive updates.",
            "Tip: After a run, the best timetable is listed here (conflict groups use row colors).",
        )
        if 0 <= index < len(tips):
            self.status_bar.showMessage(tips[index])

    def update_progress(self, gen, fitness, current_best):
        self.control_tab.update_status(f"Running — generation {gen}")
        self.control_tab.update_progress(gen)
        self.control_tab.log(f"Gen {gen:03d} | Best Fitness: {fitness:.4f}")
        self.gen_data.append(gen)
        self.fitness_data.append(fitness)
        self.graph_tab.update_graph(self.gen_data, self.fitness_data)

    def ga_finished(self, final_timetable, final_fitness):
        self.control_tab.update_progress(200)
        self.control_tab.set_running(False)
        if final_fitness == 1.0:
            self.control_tab.update_status(
                "Finished — conflict-free timetable (fitness 1.0)",
                "font-size: 18px; font-weight: bold; color: #4ec9b0;",
            )
        else:
            self.control_tab.update_status(
                "Finished — best effort schedule (some constraints may remain)",
                "font-size: 18px; font-weight: bold; color: #ce9178;",
            )
        self.results_tab.populate(final_timetable, final_fitness)
        self.tabs.setCurrentIndex(3)
