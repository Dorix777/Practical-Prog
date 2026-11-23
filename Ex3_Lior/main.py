import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QLineEdit, QComboBox, QMessageBox
)
from Account import Account
from About import AboutWindow


class BankApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bank App")
        self.setGeometry(300, 200, 360, 420)

        self.accounts = {}
        self.about_window = None

        self.label_id = QLabel("ID:", self)
        self.label_id.setGeometry(30, 30, 80, 30)

        self.id_input = QLineEdit(self)
        self.id_input.setGeometry(120, 30, 100, 30)

        self.btn_open = QPushButton("פתח חשבון", self)
        self.btn_open.setGeometry(230, 30, 100, 30)
        self.btn_open.clicked.connect(self.create_account)

        self.label_select = QLabel("חשבון:", self)
        self.label_select.setGeometry(30, 80, 80, 30)

        self.combo = QComboBox(self)
        self.combo.setGeometry(120, 80, 210, 30)
        self.combo.currentTextChanged.connect(self.update_display)

        self.label_bal = QLabel("יתרה:", self)
        self.label_bal.setGeometry(30, 130, 80, 30)

        self.balance_display = QLineEdit("", self)
        self.balance_display.setGeometry(120, 130, 210, 30)
        self.balance_display.setReadOnly(True)
        self.balance_display.setStyleSheet("background-color: lightgray;")

        self.label_amt = QLabel("סכום:", self)
        self.label_amt.setGeometry(30, 180, 80, 30)

        self.amount_input = QLineEdit(self)
        self.amount_input.setGeometry(120, 180, 210, 30)

        self.btn_deposit = QPushButton("הפקדה", self)
        self.btn_deposit.setGeometry(30, 230, 140, 35)
        self.btn_deposit.clicked.connect(self.deposit)

        self.btn_withdraw = QPushButton("משיכה", self)
        self.btn_withdraw.setGeometry(190, 230, 140, 35)
        self.btn_withdraw.clicked.connect(self.withdraw)

        self.btn_about = QPushButton("About", self)
        self.btn_about.setGeometry(30, 340, 300, 35)
        self.btn_about.clicked.connect(self.open_about)

    def create_account(self):
        id_num = self.id_input.text()
        if id_num == "":
            return
        if id_num in self.accounts:
            QMessageBox.warning(self, "שגיאה", "חשבון כזה קיים כבר")
            return

        self.accounts[id_num] = Account(id_num)
        self.combo.addItem(id_num)
        self.combo.setCurrentText(id_num)
        self.id_input.clear()

    def update_display(self):
        id_num = self.combo.currentText()
        if id_num in self.accounts:
            acc = self.accounts[id_num]
            self.balance_display.setText(str(acc.balance))
        else:
            self.balance_display.setText("")

    def deposit(self):
        id_num = self.combo.currentText()
        if id_num not in self.accounts:
            return

        if self.amount_input.text() == "":
            return

        amount = float(self.amount_input.text())
        acc = self.accounts[id_num]
        acc.deposit(amount)
        self.balance_display.setText(str(acc.balance))
        self.amount_input.clear()

    def withdraw(self):
        id_num = self.combo.currentText()
        if id_num not in self.accounts:
            return

        if self.amount_input.text() == "":
            return

        amount = float(self.amount_input.text())
        acc = self.accounts[id_num]

        if amount > acc.balance:
            QMessageBox.warning(self, "שגיאה", "אין מספיק כסף בחשבון")
            return

        acc.withdraw(amount)
        self.balance_display.setText(str(acc.balance))
        self.amount_input.clear()

    def open_about(self):
        self.about_window = AboutWindow()
        self.about_window.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = BankApp()
    window.show()
    app.exec()
