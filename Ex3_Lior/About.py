import sys
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QPushButton
from PySide6.QtGui import QPixmap


class AboutWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About")
        self.setGeometry(350, 200, 300, 360)

        self.image_label = QLabel(self)
        self.image_label.setGeometry(75, 20, 150, 150)
        pixmap = QPixmap("profile.png")
        self.image_label.setPixmap(pixmap.scaled(150, 150))

        self.name_label = QLabel("Lior Dori", self)
        self.name_label.setGeometry(20, 190, 260, 30)
        self.name_label.setStyleSheet("font-size: 18px; font-weight: bold;")

        self.email_label = QLabel("Email: lior.dori@example.com", self)
        self.email_label.setGeometry(20, 230, 260, 25)

        self.link_label = QLabel('<a href="https://www.linkedin.com/in/lior-dori-789582382/">LinkedIn Profile</a>', self)
        self.link_label.setGeometry(20, 265, 260, 25)
        self.link_label.setOpenExternalLinks(True)

        self.close_button = QPushButton("Close", self)
        self.close_button.setGeometry(100, 310, 100, 30)
        self.close_button.clicked.connect(self.close)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AboutWindow()
    window.show()
    app.exec()
