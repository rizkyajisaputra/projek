from pickle import FRAME
from pyexpat import model
import sys
import typing
import xlwt
from PyQt5 import QtCore, QtWidgets, QtSql, QtGui, QtPrintSupport
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QTableWidget, QTableWidgetItem, QFileDialog, QPushButton
from PyQt5.uic import loadUi
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel, QSqlRecord
from random import triangular
#from mysqlx import Session
from numpy import append
from simpful import *
import mysql.connector as mc
import mysql.connector
import pandas as pd

mydb = mc.connect(
    host="localhost",
    user="root",
    password="",
    database="karyawan_db"
)


class Login(QDialog):
    def __init__(self):
        super(Login,self).__init__()
        loadUi("login.ui",self)
        self.loginbutton.clicked.connect(self.loginfunction)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.dakunbutton.clicked.connect(self.gotocreate)

    def loginfunction(self):
        username = self.username.text()
        password = self.password.text()
        mydb = mc.connect(
            host="localhost",
            user="root",
            password="",
            database="karyawan_db"
            )
        
        mycursor = mydb.cursor()
        query = "SELECT * FROM user WHERE Username = %s AND Password = %s"
        mycursor.execute(query, (username, password))
            
            

        if mycursor.fetchone():
            self.main_menu = Menu()
            self.main_menu.show()
            self.close()
                
                
        else:
            #print("login gagal")
                #error = QLabel('Login gagal', self)
                #layout = self.layout()
                #layout.addWidget(error)
            self.login_label.setText("Username / Password 'SALAH'")

        mycursor.close()
        mydb.close()

        #except mc.Error as e:
            #print("TIDAK KONEKSI")
        
        #finally:
            #mycursor.close()
            #mydb.close()

        

    def gotocreate(self):
        createacc=CreateAcc()
        widget.addWidget(createacc)
        widget.setCurrentIndex(widget.currentIndex()+1)


class CreateAcc(QDialog):
    def __init__(self):
        super(CreateAcc,self).__init__()
        loadUi("register.ui",self)
        self.daftarbutton.clicked.connect(self.createaccfunction)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.konfirmasi.setEchoMode(QtWidgets.QLineEdit.Password)
        self.kembalibutton.clicked.connect(self.kembalifunction)
    
    def createaccfunction(self):
        mydb = mc.connect(
                host="localhost",
                user="root",
                password="",
                database="karyawan_db"
            )
        
        mycursor = mydb.cursor()

        user = self.username.text()
        pas = self.password.text()
        konf = self.konfirmasi.text()

        query = "INSERT INTO user (Username, Password) VALUES (%s, %s)"
        value = (user, pas)

        mycursor.execute(query, value)

        mydb.commit()


        username=self.username.text()
        if self.password.text()==self.konfirmasi.text():
            password=self.password.text()
            login=Login()
            widget.addWidget(login)
            widget.setCurrentIndex(widget.currentIndex()+1)
           
        else:
            self.label4.setText("Password Tidak Sama!!")

    def kembalifunction(self):
        login=Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex()-1)
            


class Menu(QDialog):

    def __init__(self):
        super(Menu,self).__init__()
        loadUi("menu.ui",self)
        self.databasebutton.clicked.connect(self.databasefunction)
        self.prosesbutton.clicked.connect(self.prosesfunction)
        self.resetbutton.clicked.connect(self.resetfunction)
        self.keluarbutton.clicked.connect(self.keluarfunction)
        self.simpanbutton.clicked.connect(self.simpanfunction)
        

    def databasefunction(self):
        
        database=Database()
        widget.addWidget(database)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def prosesfunction(self):
        nama = self.nama.text()

        FS = FuzzySystem()

        # Define fuzzy sets and linguistic variables
        S_1 = FuzzySet(function=Trapezoidal_MF(a=0, b=0, c=60, d=70), term="buruk")
        S_2 = FuzzySet(function=Triangular_MF(a=60, b=70, c=80), term="cukup")
        S_3 = FuzzySet(function=Trapezoidal_MF(a=70, b=80, c=100, d=100), term="baik")
        FS.add_linguistic_variable("Kedisiplinan", LinguisticVariable([S_1, S_2, S_3], concept="Nilai kedisiplinan", universe_of_discourse=[0,100]))
        F_1 = FuzzySet(function=Trapezoidal_MF(a=0, b=0, c=60, d=70), term="buruk")
        F_2 = FuzzySet(function=Triangular_MF(a=60, b=70, c=80), term="cukup")
        F_3 = FuzzySet(function=Trapezoidal_MF(a=70, b=80, c=100, d=100), term="baik")
        FS.add_linguistic_variable("Produktivitas", LinguisticVariable([F_1, F_2, F_3], concept="Nilai produktivitas", universe_of_discourse=[0,100]))
        L_1 = FuzzySet(function=Trapezoidal_MF(a=0, b=0, c=60, d=70), term="buruk")
        L_2 = FuzzySet(function=Triangular_MF(a=60, b=70, c=80), term="cukup")
        L_3 = FuzzySet(function=Trapezoidal_MF(a=70, b=80, c=100, d=100), term="baik")
        FS.add_linguistic_variable("Loyalitas", LinguisticVariable([L_1, L_2, L_3], concept="Nilai loyalitas", universe_of_discourse=[0,100]))
        M_1 = FuzzySet(function=Trapezoidal_MF(a=0, b=0, c=12, d=18), term="buruk")
        M_2 = FuzzySet(function=Triangular_MF(a=12, b=18, c=24), term="cukup")
        M_3 = FuzzySet(function=Trapezoidal_MF(a=18, b=24, c=36, d=36), term="baik")
        FS.add_linguistic_variable("Masa_Kerja", LinguisticVariable([M_1, M_2, M_3], concept="Nilai masa_kerja", universe_of_discourse=[0,36]))
        # Define output fuzzy sets and linguistic variable
        T_1 = FuzzySet(function=Trapezoidal_MF(a=0, b=0, c=50, d=60), term="buruk")
        T_2 = FuzzySet(function=Triangular_MF(a=60, b=65, c=70), term="cukup")
        T_3 = FuzzySet(function=Trapezoidal_MF(a=70, b=80, c=100, d=100), term="baik")
        FS.add_linguistic_variable("Kinerja", LinguisticVariable([T_1, T_2, T_3], universe_of_discourse=[0,100]))
        # Define fuzzy rules
        R1 = "IF (Kedisiplinan IS buruk) AND (Produktivitas IS buruk) AND (Loyalitas IS buruk) AND (Masa_Kerja IS buruk) THEN (Kinerja IS buruk)"
        R2 = "IF (Kedisiplinan IS cukup) AND (Produktivitas IS buruk) AND (Loyalitas IS buruk) AND (Masa_Kerja IS buruk) THEN (Kinerja IS buruk)"
        R3 = "IF (Kedisiplinan IS baik) AND (Produktivitas IS buruk) AND (Loyalitas IS buruk) AND (Masa_Kerja IS buruk) THEN (Kinerja IS buruk)"
        R4 = "IF (Kedisiplinan IS buruk) AND (Produktivitas IS cukup) AND (Loyalitas IS buruk) AND (Masa_Kerja IS buruk) THEN (Kinerja IS buruk)"
        R5 = "IF (Kedisiplinan IS cukup) AND (Produktivitas IS cukup) AND (Loyalitas IS buruk) AND (Masa_Kerja IS buruk) THEN (Kinerja IS cukup)"
        R6 = "IF (Kedisiplinan IS baik) AND (Produktivitas IS cukup) AND (Loyalitas IS buruk) AND (Masa_Kerja IS buruk) THEN (Kinerja IS cukup)"
        R7 = "IF (Kedisiplinan IS buruk) AND (Produktivitas IS baik) AND (Loyalitas IS buruk) AND (Masa_Kerja IS buruk) THEN (Kinerja IS buruk)"
        R8 = "IF (Kedisiplinan IS cukup) AND (Produktivitas IS baik) AND (Loyalitas IS buruk) AND (Masa_Kerja IS buruk) THEN (Kinerja IS cukup)"
        R9 = "IF (Kedisiplinan IS baik) AND (Produktivitas IS baik) AND (Loyalitas IS buruk) AND (Masa_Kerja IS buruk) THEN (Kinerja IS cukup)"
        R10 = "IF (Kedisiplinan IS buruk) AND (Produktivitas IS buruk) AND (Loyalitas IS cukup) AND (Masa_Kerja IS buruk) THEN (Kinerja IS buruk)"
        R11 = "IF (Kedisiplinan IS cukup) AND (Produktivitas IS buruk) AND (Loyalitas IS cukup) AND (Masa_Kerja IS buruk) THEN (Kinerja IS buruk)"
        R12 = "IF (Kedisiplinan IS baik) AND (Produktivitas IS buruk) AND (Loyalitas IS cukup) AND (Masa_Kerja IS buruk) THEN (Kinerja IS buruk)"
        R13 = "IF (Kedisiplinan IS buruk) AND (Produktivitas IS cukup) AND (Loyalitas IS cukup) AND (Masa_Kerja IS buruk) THEN (Kinerja IS buruk)"
        R14 = "IF (Kedisiplinan IS cukup) AND (Produktivitas IS cukup) AND (Loyalitas IS cukup) AND (Masa_Kerja IS buruk) THEN (Kinerja IS cukup)"
        R15 = "IF (Kedisiplinan IS baik) AND (Produktivitas IS cukup) AND (Loyalitas IS cukup) AND (Masa_Kerja IS buruk) THEN (Kinerja IS cukup)"
        R16 = "IF (Kedisiplinan IS buruk) AND (Produktivitas IS baik) AND (Loyalitas IS cukup) AND (Masa_Kerja IS buruk) THEN (Kinerja IS cukup)"
        R17 = "IF (Kedisiplinan IS cukup) AND (Produktivitas IS baik) AND (Loyalitas IS cukup) AND (Masa_Kerja IS buruk) THEN (Kinerja IS cukup)"
        R18 = "IF (Kedisiplinan IS baik) AND (Produktivitas IS baik) AND (Loyalitas IS cukup) AND (Masa_Kerja IS buruk) THEN (Kinerja IS baik)"
        R19 = "IF (Kedisiplinan IS buruk) AND (Produktivitas IS buruk) AND (Loyalitas IS baik) AND (Masa_Kerja IS buruk) THEN (Kinerja IS buruk)"
        R20 = "IF (Kedisiplinan IS cukup) AND (Produktivitas IS buruk) AND (Loyalitas IS baik) AND (Masa_Kerja IS buruk) THEN (Kinerja IS buruk)"
        R21 = "IF (Kedisiplinan IS baik) AND (Produktivitas IS buruk) AND (Loyalitas IS baik) AND (Masa_Kerja IS buruk) THEN (Kinerja IS cukup)"
        R22 = "IF (Kedisiplinan IS buruk) AND (Produktivitas IS cukup) AND (Loyalitas IS baik) AND (Masa_Kerja IS buruk) THEN (Kinerja IS buruk)"
        R23 = "IF (Kedisiplinan IS cukup) AND (Produktivitas IS cukup) AND (Loyalitas IS baik) AND (Masa_Kerja IS buruk) THEN (Kinerja IS cukup)"
        R24 = "IF (Kedisiplinan IS baik) AND (Produktivitas IS cukup) AND (Loyalitas IS baik) AND (Masa_Kerja IS buruk) THEN (Kinerja IS cukup)"
        R25 = "IF (Kedisiplinan IS buruk) AND (Produktivitas IS baik) AND (Loyalitas IS baik) AND (Masa_Kerja IS buruk) THEN (Kinerja IS cukup)"
        R26 = "IF (Kedisiplinan IS cukup) AND (Produktivitas IS baik) AND (Loyalitas IS baik) AND (Masa_Kerja IS buruk) THEN (Kinerja IS baik)"
        R27 = "IF (Kedisiplinan IS baik) AND (Produktivitas IS baik) AND (Loyalitas IS baik) AND (Masa_Kerja IS buruk) THEN (Kinerja IS baik)"
        R28 = "IF (Kedisiplinan IS buruk) AND (Produktivitas IS buruk) AND (Loyalitas IS buruk) AND (Masa_Kerja IS cukup) THEN (Kinerja IS buruk)"
        R29 = "IF (Kedisiplinan IS cukup) AND (Produktivitas IS buruk) AND (Loyalitas IS buruk) AND (Masa_Kerja IS cukup) THEN (Kinerja IS buruk)"
        R30 = "IF (Kedisiplinan IS baik) AND (Produktivitas IS buruk) AND (Loyalitas IS buruk) AND (Masa_Kerja IS cukup) THEN (Kinerja IS buruk)"
        R31 = "IF (Kedisiplinan IS buruk) AND (Produktivitas IS cukup) AND (Loyalitas IS buruk) AND (Masa_Kerja IS cukup) THEN (Kinerja IS buruk)"
        R32 = "IF (Kedisiplinan IS cukup) AND (Produktivitas IS cukup) AND (Loyalitas IS buruk) AND (Masa_Kerja IS cukup) THEN (Kinerja IS cukup)"
        R33 = "IF (Kedisiplinan IS baik) AND (Produktivitas IS cukup) AND (Loyalitas IS buruk) AND (Masa_Kerja IS cukup) THEN (Kinerja IS cukup)"
        R34 = "IF (Kedisiplinan IS buruk) AND (Produktivitas IS baik) AND (Loyalitas IS buruk) AND (Masa_Kerja IS cukup) THEN (Kinerja IS cukup)"
        R35 = "IF (Kedisiplinan IS cukup) AND (Produktivitas IS baik) AND (Loyalitas IS buruk) AND (Masa_Kerja IS cukup) THEN (Kinerja IS baik)"
        R36 = "IF (Kedisiplinan IS baik) AND (Produktivitas IS baik) AND (Loyalitas IS buruk) AND (Masa_Kerja IS cukup) THEN (Kinerja IS baik)"
        R37 = "IF (Kedisiplinan IS buruk) AND (Produktivitas IS buruk) AND (Loyalitas IS cukup) AND (Masa_Kerja IS cukup) THEN (Kinerja IS buruk)"
        R38 = "IF (Kedisiplinan IS cukup) AND (Produktivitas IS buruk) AND (Loyalitas IS cukup) AND (Masa_Kerja IS cukup) THEN (Kinerja IS cukup)"
        R39 = "IF (Kedisiplinan IS baik) AND (Produktivitas IS buruk) AND (Loyalitas IS cukup) AND (Masa_Kerja IS cukup) THEN (Kinerja IS cukup)"
        R40 = "IF (Kedisiplinan IS buruk) AND (Produktivitas IS cukup) AND (Loyalitas IS cukup) AND (Masa_Kerja IS cukup) THEN (Kinerja IS cukup)"
        R41 = "IF (Kedisiplinan IS cukup) AND (Produktivitas IS cukup) AND (Loyalitas IS cukup) AND (Masa_Kerja IS cukup) THEN (Kinerja IS cukup)"
        R42 = "IF (Kedisiplinan IS baik) AND (Produktivitas IS cukup) AND (Loyalitas IS cukup) AND (Masa_Kerja IS cukup) THEN (Kinerja IS cukup)"
        R43 = "IF (Kedisiplinan IS buruk) AND (Produktivitas IS baik) AND (Loyalitas IS cukup) AND (Masa_Kerja IS cukup) THEN (Kinerja IS cukup)"
        R44 = "IF (Kedisiplinan IS cukup) AND (Produktivitas IS baik) AND (Loyalitas IS cukup) AND (Masa_Kerja IS cukup) THEN (Kinerja IS baik)"
        R45 = "IF (Kedisiplinan IS baik) AND (Produktivitas IS baik) AND (Loyalitas IS cukup) AND (Masa_Kerja IS cukup) THEN (Kinerja IS baik)"
        R46 = "IF (Kedisiplinan IS buruk) AND (Produktivitas IS buruk) AND (Loyalitas IS baik) AND (Masa_Kerja IS cukup) THEN (Kinerja IS cukup)"
        R47 = "IF (Kedisiplinan IS cukup) AND (Produktivitas IS buruk) AND (Loyalitas IS baik) AND (Masa_Kerja IS cukup) THEN (Kinerja IS cukup)"
        R48 = "IF (Kedisiplinan IS baik) AND (Produktivitas IS buruk) AND (Loyalitas IS baik) AND (Masa_Kerja IS cukup) THEN (Kinerja IS cukup)"
        R49 = "IF (Kedisiplinan IS buruk) AND (Produktivitas IS cukup) AND (Loyalitas IS baik) AND (Masa_Kerja IS cukup) THEN (Kinerja IS cukup)"
        R50 = "IF (Kedisiplinan IS cukup) AND (Produktivitas IS cukup) AND (Loyalitas IS baik) AND (Masa_Kerja IS cukup) THEN (Kinerja IS cukup)"
        R51 = "IF (Kedisiplinan IS baik) AND (Produktivitas IS cukup) AND (Loyalitas IS baik) AND (Masa_Kerja IS cukup) THEN (Kinerja IS cukup)"
        R52 = "IF (Kedisiplinan IS buruk) AND (Produktivitas IS baik) AND (Loyalitas IS baik) AND (Masa_Kerja IS cukup) THEN (Kinerja IS cukup)"
        R53 = "IF (Kedisiplinan IS cukup) AND (Produktivitas IS baik) AND (Loyalitas IS baik) AND (Masa_Kerja IS cukup) THEN (Kinerja IS baik)"
        R54 = "IF (Kedisiplinan IS baik) AND (Produktivitas IS baik) AND (Loyalitas IS baik) AND (Masa_Kerja IS cukup) THEN (Kinerja IS baik)"
        R55 = "IF (Kedisiplinan IS buruk) AND (Produktivitas IS buruk) AND (Loyalitas IS buruk) AND (Masa_Kerja IS cukup) THEN (Kinerja IS buruk)"
        R56 = "IF (Kedisiplinan IS cukup) AND (Produktivitas IS buruk) AND (Loyalitas IS buruk) AND (Masa_Kerja IS cukup) THEN (Kinerja IS buruk)"
        R57 = "IF (Kedisiplinan IS baik) AND (Produktivitas IS buruk) AND (Loyalitas IS buruk) AND (Masa_Kerja IS baik) THEN (Kinerja IS cukup)"
        R58 = "IF (Kedisiplinan IS buruk) AND (Produktivitas IS cukup) AND (Loyalitas IS buruk) AND (Masa_Kerja IS baik) THEN (Kinerja IS cukup)"
        R59 = "IF (Kedisiplinan IS cukup) AND (Produktivitas IS cukup) AND (Loyalitas IS buruk) AND (Masa_Kerja IS baik) THEN (Kinerja IS baik)"
        R60 = "IF (Kedisiplinan IS baik) AND (Produktivitas IS cukup) AND (Loyalitas IS buruk) AND (Masa_Kerja IS baik) THEN (Kinerja IS baik)"
        R61 = "IF (Kedisiplinan IS buruk) AND (Produktivitas IS baik) AND (Loyalitas IS buruk) AND (Masa_Kerja IS baik) THEN (Kinerja IS cukup)"
        R62 = "IF (Kedisiplinan IS cukup) AND (Produktivitas IS baik) AND (Loyalitas IS buruk) AND (Masa_Kerja IS baik) THEN (Kinerja IS baik)"
        R63 = "IF (Kedisiplinan IS baik) AND (Produktivitas IS baik) AND (Loyalitas IS buruk) AND (Masa_Kerja IS baik) THEN (Kinerja IS baik)"
        R64 = "IF (Kedisiplinan IS buruk) AND (Produktivitas IS buruk) AND (Loyalitas IS cukup) AND (Masa_Kerja IS baik) THEN (Kinerja IS cukup)"
        R65 = "IF (Kedisiplinan IS cukup) AND (Produktivitas IS buruk) AND (Loyalitas IS cukup) AND (Masa_Kerja IS baik) THEN (Kinerja IS cukup)"
        R66 = "IF (Kedisiplinan IS baik) AND (Produktivitas IS buruk) AND (Loyalitas IS cukup) AND (Masa_Kerja IS baik) THEN (Kinerja IS cukup)"
        R67 = "IF (Kedisiplinan IS buruk) AND (Produktivitas IS cukup) AND (Loyalitas IS cukup) AND (Masa_Kerja IS baik) THEN (Kinerja IS baik)"
        R68 = "IF (Kedisiplinan IS cukup) AND (Produktivitas IS cukup) AND (Loyalitas IS cukup) AND (Masa_Kerja IS baik) THEN (Kinerja IS baik)"
        R69 = "IF (Kedisiplinan IS baik) AND (Produktivitas IS cukup) AND (Loyalitas IS cukup) AND (Masa_Kerja IS baik) THEN (Kinerja IS baik)"
        R70 = "IF (Kedisiplinan IS buruk) AND (Produktivitas IS baik) AND (Loyalitas IS cukup) AND (Masa_Kerja IS baik) THEN (Kinerja IS baik)"
        R71 = "IF (Kedisiplinan IS cukup) AND (Produktivitas IS baik) AND (Loyalitas IS cukup) AND (Masa_Kerja IS baik) THEN (Kinerja IS baik)"
        R72 = "IF (Kedisiplinan IS baik) AND (Produktivitas IS baik) AND (Loyalitas IS cukup) AND (Masa_Kerja IS baik) THEN (Kinerja IS baik)"
        R73 = "IF (Kedisiplinan IS buruk) AND (Produktivitas IS buruk) AND (Loyalitas IS baik) AND (Masa_Kerja IS baik) THEN (Kinerja IS cukup)"
        R74 = "IF (Kedisiplinan IS cukup) AND (Produktivitas IS buruk) AND (Loyalitas IS baik) AND (Masa_Kerja IS baik) THEN (Kinerja IS cukup)"
        R75 = "IF (Kedisiplinan IS baik) AND (Produktivitas IS buruk) AND (Loyalitas IS baik) AND (Masa_Kerja IS baik) THEN (Kinerja IS baik)"
        R76 = "IF (Kedisiplinan IS buruk) AND (Produktivitas IS cukup) AND (Loyalitas IS baik) AND (Masa_Kerja IS baik) THEN (Kinerja IS baik)"
        R77 = "IF (Kedisiplinan IS cukup) AND (Produktivitas IS cukup) AND (Loyalitas IS baik) AND (Masa_Kerja IS baik) THEN (Kinerja IS baik)"
        R78 = "IF (Kedisiplinan IS baik) AND (Produktivitas IS cukup) AND (Loyalitas IS baik) AND (Masa_Kerja IS baik) THEN (Kinerja IS baik)"
        R79 = "IF (Kedisiplinan IS buruk) AND (Produktivitas IS baik) AND (Loyalitas IS baik) AND (Masa_Kerja IS baik) THEN (Kinerja IS baik)"
        R80 = "IF (Kedisiplinan IS cukup) AND (Produktivitas IS baik) AND (Loyalitas IS baik) AND (Masa_Kerja IS baik) THEN (Kinerja IS baik)"
        R81 = "IF (Kedisiplinan IS baik) AND (Produktivitas IS baik) AND (Loyalitas IS baik) AND (Masa_Kerja IS baik) THEN (Kinerja IS baik)"

        FS.add_rules([R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27, R28, R29, R30, R31, R32, R33, R34, R35, R36, R37, R38, R39, R40, R41, R42, R43, R44, R45, R46, R47, R48, R49, R50, R51, R52, R53, R54, R55, R56, R57, R58, R59, R60, R61, R62, R63, R64, R65, R66, R67, R68, R69, R70, R71, R72, R73, R74, R75, R76, R77, R78, R79, R80, R81])
        kd = self.kedisiplinan.text()
        pr = self.produktivitas.text()
        ly = self.loyalitas.text()
        mk = self.masakerja.text()
        # Set antecedents values
        FS.set_variable("Kedisiplinan", kd)
        FS.set_variable("Produktivitas", pr)
        FS.set_variable("Loyalitas", ly)
        FS.set_variable("Masa_Kerja", mk)
        # Perform Mamdani inference and print output
        a = FS.Mamdani_inference(["Kinerja"])
        b = dict.values(a)
        c = float([x for x in b][0])
        #print(dict.values(a))
        print ("Nilai", c)
        d = f"{c:.4f}"
        self.kinerja.setText(str(d))

        if (c) < 70:
            self.kinerja2.setText("Tak diperpanjang")
        if (c) > 69 < 80:
            self.kinerja2.setText("Diperhitungkan")
        if (c) > 79:
            self.kinerja2.setText("Diperpanjang")
        

    def resetfunction(self):
        self.kedisiplinan.clear()
        self.produktivitas.clear()
        self.loyalitas.clear()
        self.kinerja.clear()
        self.id.clear()
        self.nama.clear()
        self.masakerja.clear()
        self.kinerja2.clear()

    def simpanfunction(self):
        try:
            

            mycursor = mydb.cursor()

            id = self.id.text()
            nama = self.nama.text()
            kedisiplinan = self.kedisiplinan.text()
            produktivitas = self.produktivitas.text()
            loyalitas = self.loyalitas.text()
            masakerja = self.masakerja.text()
            kinerja = self.kinerja.text()
            rekomendasi = self.kinerja2.text()

            query = "INSERT INTO nilai_karyawan (ID, Nama, Kedisiplinan, Produktivitas, Loyalitas, Masa_Kerja, Kinerja, Rekomendasi) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            value = (id, nama, kedisiplinan, produktivitas, loyalitas, masakerja, kinerja, rekomendasi)

            mycursor.execute(query, value)

            mydb.commit()
            self.labelResult.setText("Save Data 'BERHASIL'")

        except mc.Error as e:
            self.labelResult.setText("Save Data 'GAGAL'")

    def keluarfunction(self, Dialog):
        login=Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex()-1)
        
        


class Database(QDialog):
    def __init__(self):
        super(Database,self).__init__()
        loadUi("tabel.ui",self)
        #self.pilihbutton.clicked.connect(self.pilihfunction)
        #self.tableWidget.cellClicked.connect(self.getClickedCell)
        self.deletebutton.clicked.connect(self.deletefunction)
        self.refreshbutton.clicked.connect(self.loaddata)
        self.kembalibutton.clicked.connect(self.kembalifunction)
        self.reportbutton.clicked.connect(self.savefile)
        #self.add_data_to_sheet()
        self.initUI()

    #def getClickedCell(self, row, column):
        #print('clicked!', row, column)

    def deletefunction(self, removeRow):
        selected_row = self.tableWidget.currentRow()
        if selected_row>= 0:
            row_id = int(self.tableWidget.item(selected_row, 0).text())

            mydb = mc.connect(
                host="localhost",
                user="root",
                password="",
                database="karyawan_db"
            )
            mycursor = mydb.cursor()

            mycursor.execute("DELETE FROM nilai_karyawan WHERE ID = %s", (row_id,))
            mydb.commit()
            mydb.close()
            
    
        
        
        
    def loaddata(self):
        try:
            mydb = mc.connect(
                host="localhost",
                user="root",
                password="",
                database="karyawan_db"
            )
            mycursor = mydb.cursor()
            mycursor.execute("SELECT * FROM nilai_karyawan".format())

            result = mycursor.fetchall()

            self.tableWidget.setRowCount(0)

            for row_number, row_data in enumerate(result):
                self.tableWidget.insertRow(row_number)

                for column_number, data in enumerate(row_data):
                    self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        except mc.Error as e:
            print("Error cok!!")

    def initUI(self):
        #self.central_widget = QWidget()
        #self.central_widget(self.central_widget)

        #self.tableWidget = QTableWidget(self)
        #self.tableWidget.setRowCount(8)
        #self.tableWidget.setColumnCount(20)

        for i in range(8):
            for j in range(20):
                item = QTableWidgetItem(f'Item {i}-{j}')
                self.tableWidget.setItem(i, j, item)
        
        #self.reportbutton = QPushButton('Export to Excel', self)
        

    def savefile(self):
        columHeader = []

        for j in range(self.tableWidget.model().columnCount()):
            columHeader.append(self.tableWidget.horizontalHeaderItem(j).text())

        df = pd.DataFrame(columns=columHeader)


        filename = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File', '', ".xlsx (*.xlsx)")
        
        for row in range(self.tableWidget.rowCount()):
            for col in range(self.tableWidget.columnCount()):
                df.at[row, columHeader[col]] = self.tableWidget.item(row, col).text()
            
            df.to_excel('laporan.xlsx', index=False)
            df.to_excel('lapor.xlsx', index=False)
            df.to_excel('laporan2.xlsx', index=False)
            df.to_excel('laporan3.xlsx', index=False)
            print('excel exported')
            self.reportlabel.setText("Berhasil Export File")

    


        #for currentColumn in range(self.tableWidget.columnCount()):
            #for currentRow in range(self.tableWidget.rowCount()):
                #try:
                    #teext = str(self.tableWidget.item(currentRow, currentColumn).text())
                    #sheet.write(currentRow, currentColumn, teext)
                #except AttributeError:
                    #pass
        #wbk.save(filename)


    def kembalifunction(self):
        widget.setCurrentIndex(widget.currentIndex()-1)


app=QApplication(sys.argv)
mainwindow=Login()
widget=QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedWidth(800)
widget.setFixedHeight(620)
widget.show()
sys.exit(app.exec_())