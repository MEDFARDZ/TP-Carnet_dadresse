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
        self.delete_button.clicked.connect(self.delete_contact)
        button_layout.addWidget(self.delete_button)

        self.exit_button = QPushButton("Quitter")
        self.exit_button.clicked.connect(self.close)
        button_layout.addWidget(self.exit_button)



        self.init_button = QPushButton("Initialiser")
        self.init_button.clicked.connect(self.initialize_database)
        button_layout.addWidget(self.init_button)

        layout.addWidget(self.table)
        layout.addLayout(button_layout)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def load_contacts(self):
        self.cursor.execute("SELECT * FROM contacts")
        for contact in self.cursor.fetchall():
            self.add_contact_to_table(contact)

    def add_contact_to_table(self, contact):
        row = self.table.rowCount()
        self.table.insertRow(row)
        for i, value in enumerate(contact):
            self.table.setItem(row, i, QTableWidgetItem(value))

    def add_contact(self):
        dialog = AddContactDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            name, surname, phone, email = dialog.get_contact_info()
            self.cursor.execute("INSERT INTO contacts VALUES (?, ?, ?, ?)", (name, surname, phone, email))
            self.db_connection.commit()
            self.add_contact_to_table((name, surname, phone, email))

    def edit_contact(self):
        row = self.table.currentRow()
        if row != -1:
            name, surname, phone, email = [self.table.item(row, i).text() if self.table.item(row, i) is not None else "" for i in range(4)]
            dialog = AddContactDialog(self)
            dialog.setWindowTitle("Edit Contact")
            dialog.set_contact_info(name, surname, phone, email)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                new_name, new_surname, new_phone, new_email = dialog.get_contact_info()
                self.table.setItem(row, 0, QTableWidgetItem(new_name))
                self.table.setItem(row, 1, QTableWidgetItem(new_surname))
                self.table.setItem(row, 2, QTableWidgetItem(new_phone))
                self.table.setItem(row, 3, QTableWidgetItem(new_email))
                self.cursor.execute("UPDATE contacts SET name=?, surname=?, phone=?, email=? WHERE rowid=?", (new_name, new_surname, new_phone, new_email, row + 1))
                self.db_connection.commit()

    def delete_contact(self):
        row = self.table.currentRow()
        if row != -1:
            result = QMessageBox.question(self, "Supprimer le contact",
                                          "Êtes-vous sûr(e) de vouloir supprimer ce contact ?",
                                          QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if result == QMessageBox.StandardButton.Yes:
                # Retrieve contact details from the table
                name = self.table.item(row, 0).text() if self.table.item(row, 0) is not None else ""
                surname = self.table.item(row, 1).text() if self.table.item(row, 1) is not None else ""
                phone = self.table.item(row, 2).text() if self.table.item(row, 2) is not None else ""
                email = self.table.item(row, 3).text() if self.table.item(row, 3) is not None else ""

                # Use a unique identifier for deletion, like phone or email
                self.cursor.execute("DELETE FROM contacts WHERE phone=? OR email=?", (phone, email))
                self.db_connection.commit()

                # Remove the row from the table
                self.table.removeRow(row)
    def reload_contacts(self):
        self.table.setRowCount(0)  # Clear the current data in the table
        self.load_contacts()  # Reload the data from the database



    def initialize_database(self):
        # Drop the existing table and create a new one
        self.cursor.execute("DROP TABLE IF EXISTS contacts")
        self.cursor.execute('''CREATE TABLE contacts 
                               (name TEXT, surname TEXT, phone TEXT, email TEXT)''')
        self.db_connection.commit()
        self.reload_contacts()  # Refresh the UI to reflect database changes
        QMessageBox.information(self, "Base de données initialisée", "La base de données a été réinitialisée à son état initial.")

    def closeEvent(self, event):
        self.db_connection.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ContactManager()
    window.show()
    sys.exit(app.exec())

