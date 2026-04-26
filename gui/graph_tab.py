from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

class GraphTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 12)
        layout.setSpacing(10)
        self.chart_hint = QLabel(
            "Best fitness score by generation. Start a run from the Run tab; each generation appends a point here."
        )
        self.chart_hint.setObjectName("pageSubtitle")
        self.chart_hint.setWordWrap(True)
        layout.addWidget(self.chart_hint)
        plt.style.use('dark_background')
        self.figure = Figure(facecolor='#1e1e1e')
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_facecolor('#1e1e1e')
        self.ax.set_title("Evolution Tracking", color='#4fc1ff', fontsize=14, fontweight='bold')
        self.ax.set_xlabel("Generation", color='#cccccc')
        self.ax.set_ylabel("Fitness Score", color='#cccccc')
        self.ax.grid(True, color='#333333', linestyle='--')
        self.ax.tick_params(colors='#cccccc')
        layout.addWidget(self.canvas)
        self.line, = self.ax.plot([], [], color='#00d1ff', linewidth=2.5, marker='o', markersize=4, markerfacecolor='#ffffff')

    def update_graph(self, gen_data, fitness_data):
        self.line.set_data(gen_data, fitness_data)
        self.ax.relim()
        self.ax.autoscale_view()
        self.canvas.draw()

    def clear(self):
        self.ax.clear()
        self.ax.set_facecolor('#1e1e1e')
        self.ax.set_title("Evolution Tracking", color='#4fc1ff', fontsize=14, fontweight='bold')
        self.ax.set_xlabel("Generation", color='#cccccc')
        self.ax.set_ylabel("Fitness Score", color='#cccccc')
        self.ax.grid(True, color='#333333', linestyle='--')
        self.ax.tick_params(colors='#cccccc')
        self.line, = self.ax.plot([], [], color='#00d1ff', linewidth=2.5, marker='o', markersize=4, markerfacecolor='#ffffff')
        self.canvas.draw()
