import sqlite3
import csv

from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QTableWidget, QLineEdit, QTableWidgetItem

conn = sqlite3.connect("project.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS Persons (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Nom varchar(255),
    Prenom varchar(255),
    Adresse varchar(255),
    Code varchar(10),
    Ville varchar(255),
    Telephone varchar(255),
    Mail varchar(255)
);
""")
conn.commit()


def AfficherTout():
    cursor.execute("SELECT * FROM Persons")
    resultat = cursor.fetchall()
    tab.setRowCount(len(resultat))
    tab.setColumnCount(8)
    tab.setHorizontalHeaderLabels(['Id', 'Nom', 'Prenom', 'Adresse', 'Code', 'Ville', 'Telephone', 'Email'])

    for i in range(len(resultat)):
        for j in range(8):
            tab.setItem(i, j, QTableWidgetItem(str(resultat[i][j])))


def inserer_donnees():
    cursor.execute(
        "INSERT INTO Persons (Nom, Prenom, Adresse, Code, Ville, Telephone, Mail) VALUES (?, ?, ?, ?, ?, ?, ?);",
        (
            lineEditNom.text(),
            lineEditPrenom.text(),
            lineEditAdresse.text(),
            lineEditCode.text(),
            lineEditVille.text(),
            lineEditTelephone.text(),
            lineEditEmail.text()
        )
    )
    conn.commit()
    Annuler()

def Supprimer():
    row = tab.currentRow()
    item = tab.item(row, 0)
    if item is not None:
        id = item.text()
        cursor.execute("DELETE FROM Persons WHERE Id = ?", (id,))
        conn.commit()
        AfficherTout()
    else:
        print(f"No item at row {row}")


def Modifier():
    row = tab.currentRow()
    if row != -1:
        item = tab.item(row, 0)
        if item is not None:
            id = item.text()
            cursor.execute(
                "UPDATE Persons SET Nom = ?, Prenom = ?, Adresse = ?, Code = ?, Ville = ?, Telephone = ?, Mail = ? WHERE Id = ?",
                (
                    lineEditNom.text() if lineEditNom.text() != "" else tab.item(row, 1).text(),
                    lineEditPrenom.text() if lineEditPrenom.text() != "" else tab.item(row, 2).text(),
                    lineEditAdresse.text() if lineEditAdresse.text() != "" else tab.item(row, 3).text(),
                    lineEditCode.text() if lineEditCode.text() != "" else tab.item(row, 4).text(),
                    lineEditVille.text() if lineEditVille.text() != "" else tab.item(row, 5).text(),
                    lineEditTelephone.text() if lineEditTelephone.text() != "" else tab.item(row, 6).text(),
                    lineEditEmail.text() if lineEditEmail.text() != "" else tab.item(row, 7).text(),
                    id,
                ),
            )
            conn.commit()
            AfficherTout()

def Annuler():
    # Cette fonction efface tous les QLineEdit
    lineEditId.clear()
    lineEditNom.clear()
    lineEditPrenom.clear()
    lineEditAdresse.clear()
    lineEditCode.clear()
    lineEditVille.clear()
    lineEditTelephone.clear()
    lineEditEmail.clear()



def Imprimer():
    # Cette fonction imprime toutes les informations de la base de données dans un fichier CSV
    cursor.execute("SELECT * FROM Persons")
    resultat = cursor.fetchall()

    with open('persons.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Id', 'Nom', 'Prenom', 'Adresse', 'Code', 'Ville', 'Telephone', 'Email'])
        writer.writerows(resultat)
#2- creer une application
app = QApplication([])

#3- fenetre
fen = QWidget()

# - Btn7
btn7 = QPushButton(fen)
btn7.setText("Rechercher par ID")
btn7.setGeometry(780, 580, 130, 40)
btn7.setStyleSheet("background-color: BLUE; color: white; border-radius: 10px;")
btn7.setFont(QFont("Arial", 12))

# ...

# Définir la fonction RechercherParId après la définition de btn7
def RechercherParId():
    id_recherche = lineEditIdSearch.text()
    cursor.execute("SELECT * FROM Persons WHERE Id = ?", (id_recherche,))
    resultat1 = cursor.fetchall()
    tab.setRowCount(len(resultat1))
    tab.setColumnCount(8)
    tab.setHorizontalHeaderLabels(['Id', 'Nom', 'Prenom', 'Adresse', 'Code', 'Ville', 'Telephone', 'Email'])

    for i in range(len(resultat1)):
        for j in range(8):
            tab.setItem(i, j, QTableWidgetItem(str(resultat1[i][j])))

btn7.clicked.connect(RechercherParId)


#3- fenetre

fen = QWidget()

fen.setWindowTitle("Carnet d'adresse ")

fen.setGeometry(0, 0, 920, 800)
fen.setStyleSheet("background-color: rgb(51, 51, 51); color: white;")

#-- QTable

tab = QTableWidget(fen)
resultat = cursor.fetchall()
tab.setRowCount(len(resultat))

tab.setColumnCount(8)
tab.setGeometry(50, 130, 800, 200)
tab.setStyleSheet("background-color: rgb(255, 255, 255); color: black; border-radius: 5px;")
tab.setFont(QFont("Arial", 12))  # Remplacez "Arial" par la police que vous souhaitez et 12 par la taille de police désirée


#-- Header

tab.setHorizontalHeaderLabels(['Id', 'Nom','Prenom','Adresse', 'Code', 'Ville', 'Telephone','Email'])
header = tab.horizontalHeader()

header.setDefaultSectionSize(100)
font = header.font()
font.setPointSize(18)
header.setFont(font)

#-Label
lbl0 = QLabel(fen)

lbl0.setText("Id :")

lbl0.setGeometry(60, 380, 50, 20)
lbl0.setFont(QFont("Arial", 12))

lbl1 = QLabel(fen)

lbl1.setText("Nom :")

lbl1.setGeometry(60, 430, 50, 20)
lbl1.setFont(QFont("Arial", 12))

lbl2 = QLabel(fen)

lbl2.setText("Prenom: ")

lbl2.setGeometry(60, 480, 70, 20)
lbl2.setFont(QFont("Arial", 12))

lbl3 = QLabel(fen)

lbl3.setText("Adresse :")

lbl3.setGeometry(60, 530, 100, 20)
lbl3.setFont(QFont("Arial", 12))

lbl4 = QLabel(fen)

lbl4.setText("Code Postal :")

lbl4.setGeometry(60, 580, 100, 20)
lbl4.setFont(QFont("Arial", 12))

lbl5 = QLabel(fen)

lbl5.setText("Ville :")

lbl5.setGeometry(60, 630, 100, 20)
lbl5.setFont(QFont("Arial", 12))

lbl6 = QLabel(fen)

lbl6.setText("Telephone :")

lbl6.setGeometry(60, 680, 100, 20)
lbl6.setFont(QFont("Arial", 12))

lbl7 = QLabel(fen)

lbl7.setText("Email :")

lbl7.setGeometry(60, 730, 100, 20)
lbl7.setFont(QFont("Arial", 12))

# -- Line Edit
lineEditId = QLineEdit(fen)

lineEditId.setGeometry(180, 380, 350, 35)
lineEditId.setStyleSheet("background-color: rgb(25, 25, 25); color: white; border-radius: 5px;")
lineEditId.setFont(QFont("Arial", 12))

#lineEditId.setReadOnly(True)
lineEditNom = QLineEdit(fen)
lineEditNom.setStyleSheet("background-color: rgb(25, 25, 25); color: white; border-radius: 5px;")
lineEditNom.setFont(QFont("Arial", 12))

lineEditNom.setGeometry(180, 430, 350, 35)

lineEditPrenom = QLineEdit(fen)

lineEditPrenom.setGeometry(180, 480, 350, 35)
lineEditPrenom.setStyleSheet("background-color: rgb(25, 25, 25); color: white; border-radius: 5px;")
lineEditPrenom.setFont(QFont("Arial", 12))

lineEditAdresse = QLineEdit(fen)

lineEditAdresse.setGeometry(180, 530, 350, 35)
lineEditAdresse.setStyleSheet("background-color: rgb(25, 25, 25); color: white; border-radius: 5px;")
lineEditCode = QLineEdit(fen)
lineEditAdresse.setFont(QFont("Arial", 12))

lineEditCode.setGeometry(180, 580, 350, 35)
lineEditCode.setStyleSheet("background-color: rgb(25, 25, 25); color: white; border-radius: 5px;")
lineEditCode.setFont(QFont("Arial", 12))
lineEditVille = QLineEdit(fen)
lineEditVille.setFont(QFont("Arial", 12))

lineEditVille.setGeometry(180, 630, 350, 35)
lineEditVille.setStyleSheet("background-color: rgb(25, 25, 25); color: white; border-radius: 5px;")

lineEditTelephone = QLineEdit(fen)
lineEditTelephone.setFont(QFont("Arial", 12))

lineEditTelephone.setGeometry(180, 680, 350, 35)
lineEditTelephone.setStyleSheet("background-color: rgb(25, 25, 25); color: white; border-radius: 5px;")
lineEditEmail = QLineEdit(fen)
lineEditEmail.setFont(QFont("Arial", 12))

lineEditEmail.setGeometry(180, 730, 350, 35)
lineEditEmail.setStyleSheet("background-color: rgb(25, 25, 25); color: white; border-radius: 5px;")

#lineEditIdSearch = QLineEdit(fen)
#lineEditIdSearch.setGeometry(780, 530, 120, 30)
#lineEditIdSearch.setStyleSheet("background-color: rgb(25, 25, 25); color: white; border-radius: 5px;")
#lineEditIdSearch.setFont(QFont("Arial", 12))
#-Btn1

btn1 = QPushButton(fen)

btn1.setText("Ajouter")

btn1.setGeometry(650, 430, 120, 40)
btn1.setStyleSheet("QPushButton { background-color: BLUE; color: white; border-radius: 10px; }")
btn1.setFont(QFont("Arial", 12))  # Remplacez "Arial" par la police que vous souhaitez et 12 par la taille de police désirée

btn1.clicked.connect(inserer_donnees)

#-Btn2

btn2 = QPushButton(fen)

btn2.setText("Afficher Tout")

btn2.setGeometry(650, 480, 120, 40)
btn2.setStyleSheet("background-color: BLUE; color: white;")
btn2.setStyleSheet("QPushButton { background-color: bLUE; color: white; border-radius: 10px; }")
btn2.setFont(QFont("Arial", 12))  # Remplacez "Arial" par la police que vous souhaitez et 12 par la taille de police désirée

btn2.clicked.connect(AfficherTout)

#-Btn3

btn3 = QPushButton(fen)

btn3.setText("Modifier")

btn3.setGeometry(650, 530, 120, 40)
btn3.setStyleSheet("background-color: BLUE; color: white;")
btn3.setStyleSheet("QPushButton { background-color: grey; color: white; border-radius: 10px; }")
btn3.setFont(QFont("Arial", 12))  # Remplacez "Arial" par la police que vous souhaitez et 12 par la taille de police désirée

btn3.clicked.connect(Modifier)

#-Btn4

btn4 = QPushButton(fen)

btn4.setText("Supprimer")

btn4.setGeometry(650, 580, 120, 40)
btn4.setStyleSheet("background-color: BLUE; color: white;")
btn4.setStyleSheet("QPushButton { background-color: grey; color: white; border-radius: 10px; }")
btn4.setFont(QFont("Arial", 12))  # Remplacez "Arial" par la police que vous souhaitez et 12 par la taille de police désirée



btn4.clicked.connect(Supprimer)

#-Btn5

btn5 = QPushButton(fen)

btn5.setText("Annuler")

btn5.setGeometry(650, 630, 120, 40)
btn5.setStyleSheet("background-color: BLUE; color: white;")
btn5.setStyleSheet("QPushButton { background-color: grey; color: white; border-radius: 10px; }")
btn5.setFont(QFont("Arial", 12))  # Remplacez "Arial" par la police que vous souhaitez et 12 par la taille de police désirée

btn5.clicked.connect(Annuler)
#-Btn6

btn6 = QPushButton(fen)

btn6.setText("Imprimer")

btn6.setGeometry(650, 680, 120, 40)
btn6.setStyleSheet("background-color: BLUE; color: white;")
btn6.setStyleSheet("QPushButton { background-color: grey; color: white; border-radius: 10px; }")
btn6.setFont(QFont("Arial", 12))  # Remplacez "Arial" par la police que vous souhaitez et 12 par la taille de police désirée

btn6.clicked.connect(Imprimer)



# -- Image
qpixmap2 =QPixmap("./annuaire.jpg")
lbl_img2 = QLabel(fen)
lbl_img2.setGeometry(20, 0, 350, 110)
lbl_img2.setPixmap(qpixmap2)
# -- taille image
lbl_img2.setScaledContents(True)
lbl_img2.resize(300, 110)



#widgets
fen.show()

#-Executer
app.exec()






