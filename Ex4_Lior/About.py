from PySide6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt


class AboutWindow(QWidget):
    def __init__(self, github_url="https://github.com/Dorix777/Practical-Prog"):
        super().__init__()
        self.setWindowTitle("About")
        self.setFixedSize(320, 400)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        self.image_label = QLabel(self)
        pixmap = QPixmap("profile.png")
        if not pixmap.isNull():
            self.image_label.setPixmap(pixmap.scaled(130, 130, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.image_label)

        self.name_label = QLabel("Lior Dori", self)
        self.name_label.setObjectName("aboutName")
        self.name_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.name_label)

        self.email_label = QLabel("Email: ldori61@gmail.com", self)
        self.email_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.email_label)

        self.linkedin_label = QLabel('<a href="https://www.linkedin.com/in/lior-dori/">LinkedIn Profile</a>', self)
        self.linkedin_label.setAlignment(Qt.AlignCenter)
        self.linkedin_label.setOpenExternalLinks(True)
        layout.addWidget(self.linkedin_label)

        self.github_label = QLabel(f'<a href="{github_url}">GitHub Repository</a>', self)
        self.github_label.setAlignment(Qt.AlignCenter)
        self.github_label.setOpenExternalLinks(True)
        layout.addWidget(self.github_label)

        self.close_button = QPushButton("Close", self)
        self.close_button.clicked.connect(self.close)
        layout.addWidget(self.close_button)

        self.setLayout(layout)


if __name__ == '__main__':
    app = QApplication([])
    window = AboutWindow()
    window.show()
    app.exec()
