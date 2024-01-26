import sys
import sqlite3
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QPushButton, QLineEdit, QLabel, QMessageBox, QDialog, QHBoxLayout
from PyQt6.QtGui import QPixmap  # Add this line to import QPixmap
from PyQt6.QtCore import Qt

class AddContactDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
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


class ContactManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db_connection = sqlite3.connect('contacts.db')
        self.cursor = self.db_connection.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS contacts 
                               (name TEXT, surname TEXT, phone TEXT, email TEXT)''')
        self.init_ui()
        self.load_contacts()

    def init_ui(self):
        self.setWindowTitle("CARNET D'ADRESSES ")
        self.setGeometry(200, 200, 800, 600)


        layout = QVBoxLayout()

        # Add a QLabel to display the logo
        logo_label = QLabel(self)
        pixmap = QPixmap("bdeb.jpg")  # Change this to the path of your logo image
        pixmap = pixmap.scaled(30, 30, Qt.AspectRatioMode.KeepAspectRatio)
        logo_label.setPixmap(pixmap)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Add the logo QLabel to the layout
        layout.addWidget(logo_label)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Nom", "Prénom", "Téléphone ", "Courriel"])
        self.table.horizontalHeader().setStretchLastSection(True)

        button_layout = QHBoxLayout()
        self.add_button = QPushButton("Ajouter")
        self.add_button.clicked.connect(self.add_contact)
        button_layout.addWidget(self.add_button)

        self.edit_button = QPushButton("Éditer")
        self.edit_button.clicked.connect(self.edit_contact)
        button_layout.addWidget(self.edit_button)

        self.delete_button = QPushButton("Supprimer")
