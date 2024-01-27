mport sys
import sqlite3
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QPushButton, QLineEdit, QLabel, QMessageBox, QDialog, QHBoxLayout
from PyQt6.QtGui import QPixmap  # Add this line to import QPixmap
from PyQt6.QtCore import Qt

class AddContactDialog(QDialog):
    def _init_(self, parent=None):
        super()._init_(parent)
        self.setWindowTitle("Ajout de contact ")
        self.setFixedSize(400, 300)

        layout = QVBoxLayout()

        self.name_edit = QLineEdit()
        self.surname_edit = QLineEdit()
        self.phone_edit = QLineEdit()
        self.email_edit = QLineEdit()

        layout.addWidget(self.create_label_and_input("Nom:", self.name_edit))
        layout.addWidget(self.create_label_and_input("Prenom:", self.surname_edit))
        layout.addWidget(self.create_label_and_input("Telephone:", self.phone_edit))
        layout.addWidget(self.create_label_and_input("Email:", self.email_edit))

        buttons_layout = QHBoxLayout()
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        buttons_layout.addWidget(ok_button)

        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_button)


            def create_label_and_input(self, label_text, input_widget):
        container_widget = QWidget()
        container_layout = QHBoxLayout(container_widget)

        label = QLabel(label_text)
        label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        container_layout.addWidget(label)

        container_layout.addWidget(input_widget)
        return container_widget

    def get_contact_info(self):
        return self.name_edit.text(), self.surname_edit.text(), self.phone_edit.text(), self.email_edit.text()

    def set_contact_info(self, name, surname, phone, email):
        self.name_edit.setText(name)
        self.surname_edit.setText(surname)
        self.phone_edit.setText(phone)
        self.email_edit.setText(email)



        layout.addLayout(buttons_layout)
        self.setLayout(layout)
