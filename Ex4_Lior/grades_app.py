from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QLineEdit,
    QTableWidget, QTableWidgetItem, QFileDialog, QVBoxLayout,
    QHBoxLayout, QHeaderView, QMessageBox
)
from PySide6.QtGui import QIntValidator, QDesktopServices
from PySide6.QtCore import Qt, QUrl

try:
    from About import AboutWindow
except ImportError:
    from Ex4_Lior.About import AboutWindow


class GradesApp(QWidget):
    def __init__(self):
        super().__init__()

        self.student_ids = []
        self.original_grades = []
        self.corrected_grades = []
        self.selected_file = ''

        self.about_window = None

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

        self.btn_about = QPushButton("About")
        self.btn_about.setObjectName("aboutButton")
        self.btn_about.clicked.connect(self.open_about)
        top_buttons_layout.addWidget(self.btn_about)

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

        self.btn_update_file = QPushButton("Update File")
        self.btn_update_file.setObjectName("updateButton")
        self.btn_update_file.clicked.connect(self.update_file)
        main_layout.addWidget(self.btn_update_file)

        self.setLayout(main_layout)

    def load_stylesheet(self):
        try:
            with open("grades_style.qss", "r") as f:
                self.setStyleSheet(f.read())
        except:
            try:
                with open("Ex4_Lior/grades_style.qss", "r") as f:
                    self.setStyleSheet(f.read())
            except:
                pass

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

        with open(self.selected_file, "r") as f:
            lines = f.readlines()

        for line in lines[1:]:
            line = line.strip()
            if line:
                parts = line.split(",")
                self.student_ids.append(parts[0])
                self.original_grades.append(int(parts[1]))

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

    def update_file(self):
        if not self.selected_file:
            QMessageBox.warning(self, "Warning", "Please select a file first!")
            return

        with open(self.selected_file, "w") as f:
            f.write("ID,Grade\n")
            for i in range(len(self.student_ids)):
                f.write(f"{self.student_ids[i]},{self.corrected_grades[i]}\n")

        QDesktopServices.openUrl(QUrl.fromLocalFile(self.selected_file))

    def open_about(self):
        if self.about_window is None:
            self.about_window = AboutWindow()
        self.about_window.show()


if __name__ == "__main__":
    app = QApplication([])
    window = GradesApp()
    window.show()
    app.exec()
