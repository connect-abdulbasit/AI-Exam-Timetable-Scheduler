from PyQt5.QtWidgets import QMainWindow, QTabWidget, QMessageBox
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
        self.setGeometry(100, 100, 1200, 850)
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
        self.tabs.addTab(self.config_tab, "Configuration")
        self.tabs.addTab(self.control_tab, "Control Panel")
        self.tabs.addTab(self.graph_tab, "Live Visualization")
        self.tabs.addTab(self.results_tab, "Optimized Timetable")

    def start_ga(self):
        errors = self.config.validate()
        if errors:
            QMessageBox.warning(self, "Configuration Error", "Issues:\n" + "\n".join(errors))
            return
        self.control_tab.set_running(True)
        self.control_tab.clear_logs()
        self.gen_data.clear()
        self.fitness_data.clear()
        self.graph_tab.clear()
        self.results_tab.clear()
        self.worker = GAWorker(self.config)
        self.worker.progress_update.connect(self.update_progress)
        self.worker.finished_signal.connect(self.ga_finished)
        self.worker.start()

    def update_progress(self, gen, fitness, current_best):
        self.control_tab.update_status(f"Status: Evolving... Generation {gen}")
        self.control_tab.update_progress(gen)
        self.control_tab.log(f"Gen {gen:03d} | Best Fitness: {fitness:.4f}")
        self.gen_data.append(gen)
        self.fitness_data.append(fitness)
        self.graph_tab.update_graph(self.gen_data, self.fitness_data)

    def ga_finished(self, final_timetable, final_fitness):
        self.control_tab.update_progress(200)
        self.control_tab.set_running(False)
        if final_fitness == 1.0:
            self.control_tab.update_status("Status: SUCCESS! Conflict-free timetable found.", 
                                         "font-size: 18px; font-weight: bold; color: #4ec9b0;")
        else:
            self.control_tab.update_status("Status: FINISHED (Partial Success)", 
                                         "font-size: 18px; font-weight: bold; color: #ce9178;")
        self.results_tab.populate(final_timetable)
        self.tabs.setCurrentIndex(3)
