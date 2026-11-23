import sys
import os
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PySide6.QtCore import Qt


class GradesApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_stylesheet()

    def init_ui(self):
        self.setWindowTitle("Student Grades Adjustment")
        self.resize(650, 700)

        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)

        title_label = QLabel("Student Grades Management & Bonus System")
        title_label.setObjectName("headerTitle")
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        self.setLayout(main_layout)

    def load_stylesheet(self):
        qss_path = os.path.join(os.path.dirname(__file__), "grades_style.qss")
        if os.path.exists(qss_path):
            with open(qss_path, "r", encoding="utf-8") as f:
                self.setStyleSheet(f.read())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GradesApp()
    window.show()
    sys.exit(app.exec())
