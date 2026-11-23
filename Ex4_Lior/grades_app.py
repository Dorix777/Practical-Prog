import sys
import os
import csv
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QLineEdit,
    QTableWidget, QTableWidgetItem, QFileDialog,
    QVBoxLayout, QHBoxLayout, QHeaderView
)
from PySide6.QtGui import QIntValidator
from PySide6.QtCore import Qt


class GradesApp(QWidget):
    def __init__(self):
        super().__init__()

        self.student_ids = []
        self.original_grades = []
        self.corrected_grades = []
        self.selected_file = ''

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

        top_buttons_layout = QHBoxLayout()

        self.btn_load_file = QPushButton("Select Grades File")
        self.btn_load_file.clicked.connect(self.load_file)
        top_buttons_layout.addWidget(self.btn_load_file)

        main_layout.addLayout(top_buttons_layout)

        bonus_layout = QHBoxLayout()
        bonus_label = QLabel("Correction Points (Press Enter):")

        self.bonus_input = QLineEdit()
        self.bonus_input.setPlaceholderText("Enter integer and press Enter...")
        self.bonus_input.setValidator(QIntValidator(-100, 100, self))
        self.bonus_input.returnPressed.connect(self.apply_bonus)

        bonus_layout.addWidget(bonus_label)
        bonus_layout.addWidget(self.bonus_input)
        main_layout.addLayout(bonus_layout)

        self.table = QTableWidget(50, 3)
        self.table.setHorizontalHeaderLabels(["ID", "Original Grades", "Corrected Grades"])
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        main_layout.addWidget(self.table)

        self.setLayout(main_layout)

    def load_stylesheet(self):
        qss_path = os.path.join(os.path.dirname(__file__), "grades_style.qss")
        if os.path.exists(qss_path):
            with open(qss_path, "r", encoding="utf-8") as f:
                self.setStyleSheet(f.read())

    def load_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Grades File", "", "CSV Files (*.csv);;All Files (*)"
        )
        if not file_path:
            return

        self.selected_file = file_path
        self.student_ids = []
        self.original_grades = []
        self.corrected_grades = []

        with open(self.selected_file, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader, None)
            for row in reader:
                if row and len(row) >= 2:
                    self.student_ids.append(row[0].strip())
                    self.original_grades.append(int(float(row[1].strip())))

        self.corrected_grades = list(self.original_grades)
        self.update_table()

    def update_table(self):
        self.table.clearContents()
        total_rows = max(50, len(self.student_ids))
        self.table.setRowCount(total_rows)

        for row in range(len(self.student_ids)):
            id_item = QTableWidgetItem(str(self.student_ids[row]))
            orig_item = QTableWidgetItem(str(self.original_grades[row]))
            corr_item = QTableWidgetItem(str(self.corrected_grades[row]))

            id_item.setTextAlignment(Qt.AlignCenter)
            orig_item.setTextAlignment(Qt.AlignCenter)
            corr_item.setTextAlignment(Qt.AlignCenter)

            self.table.setItem(row, 0, id_item)
            self.table.setItem(row, 1, orig_item)
            self.table.setItem(row, 2, corr_item)

    def apply_bonus(self):
        text = self.bonus_input.text().strip()
        if not text:
            return

        try:
            bonus = int(text)
        except ValueError:
            return

        self.corrected_grades = []
        for orig in self.original_grades:
            new_grade = orig + bonus
            if new_grade > 100:
                new_grade = 100
            elif new_grade < 0:
                new_grade = 0
            self.corrected_grades.append(new_grade)

        self.update_table()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GradesApp()
    window.show()
    sys.exit(app.exec())
