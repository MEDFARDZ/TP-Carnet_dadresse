import sys
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

        layout.addLayout(buttons_layout)
        self.setLayout(layout)
