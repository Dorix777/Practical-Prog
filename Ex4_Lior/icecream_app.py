import sys
import os
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PySide6.QtCore import Qt


class IceCreamApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_stylesheet()

    def init_ui(self):
        self.setWindowTitle("Ice Cream Revenue vs Temperature")
        self.resize(750, 600)

        main_layout = QVBoxLayout()
        main_layout.setSpacing(12)

        title_label = QLabel("Ice Cream Revenue Analysis")
        title_label.setObjectName("headerTitle")
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        self.setLayout(main_layout)

    def load_stylesheet(self):
        qss_path = os.path.join(os.path.dirname(__file__), "icecream_style.qss")
        if os.path.exists(qss_path):
            with open(qss_path, "r", encoding="utf-8") as f:
                self.setStyleSheet(f.read())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = IceCreamApp()
    window.show()
    sys.exit(app.exec())
