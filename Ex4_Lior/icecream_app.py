import sys
import os
import csv
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QFileDialog, QVBoxLayout, QHBoxLayout
)
from PySide6.QtCore import Qt

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from About import AboutWindow


class IceCreamApp(QWidget):
    def __init__(self):
        super().__init__()
        self.temperatures = []
        self.revenues = []
        self.about_window = None

        self.init_ui()
        self.load_stylesheet()
        self.draw_temp_plot()

    def init_ui(self):
        self.setWindowTitle("Ice Cream Revenue vs Temperature")
        self.resize(750, 650)

        main_layout = QVBoxLayout()
        main_layout.setSpacing(12)

        title_label = QLabel("Ice Cream Revenue Analysis")
        title_label.setObjectName("headerTitle")
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        top_buttons_layout = QHBoxLayout()

        self.btn_load_file = QPushButton("Select Ice Cream CSV File")
        self.btn_load_file.clicked.connect(self.load_file)
        top_buttons_layout.addWidget(self.btn_load_file)

        self.btn_about = QPushButton("About")
        self.btn_about.setObjectName("aboutButton")
        self.btn_about.clicked.connect(self.open_about)
        top_buttons_layout.addWidget(self.btn_about)

        main_layout.addLayout(top_buttons_layout)

        self.figure = Figure(figsize=(7, 5), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.ax = self.figure.add_subplot(111)

        main_layout.addWidget(self.toolbar)
        main_layout.addWidget(self.canvas)

        self.setLayout(main_layout)

    def load_stylesheet(self):
        qss_path = os.path.join(os.path.dirname(__file__), "icecream_style.qss")
        if os.path.exists(qss_path):
            with open(qss_path, "r", encoding="utf-8") as f:
                self.setStyleSheet(f.read())

    def draw_temp_plot(self):
        self.ax.clear()
        self.ax.plot([0, 10, 20, 30, 40], [0, 200, 400, 600, 800], color='gray', linestyle='--')
        self.ax.set_title("Preview (Please select a CSV file to display data)")
        self.ax.set_xlabel("Temperature")
        self.ax.set_ylabel("Revenue")
        self.canvas.draw()

    def load_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Ice Cream CSV File", "", "CSV Files (*.csv);;All Files (*)"
        )
        if not file_path:
            return

        self.temperatures = []
        self.revenues = []

        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                if row and len(row) >= 2:
                    self.temperatures.append(float(row[0].strip()))
                    self.revenues.append(float(row[1].strip()))

        self.draw_graph()

    def draw_graph(self):
        if not self.temperatures or not self.revenues:
            return

        self.ax.clear()
        self.ax.scatter(self.temperatures, self.revenues, s=1, color='#2b6cb0', label='Daily Revenue')

        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)

        self.ax.set_title("Ice Cream Revenue vs Outside Temperature", fontsize=13, fontweight='bold', pad=12)
        self.ax.set_xlabel("Outside Temperature (°C)", fontsize=11)
        self.ax.set_ylabel("Ice Cream Revenue ($)", fontsize=11)

        self.ax.legend(loc='upper left', frameon=False)
        self.canvas.draw()

    def open_about(self):
        if self.about_window is None:
            self.about_window = AboutWindow()
        self.about_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = IceCreamApp()
    window.show()
    sys.exit(app.exec())
