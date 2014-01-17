'''


@author: Phate

Aenderungen/Hinzufuegen:




'''
import pickle
import sys
import PyQt5.QtCore
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal
from hauptfenster import Ui_MainWindow as muh
from PyQt5.QtWidgets import (QAction, QMessageBox)


class MeinFenster(PyQt5.QtWidgets.QMainWindow, muh):
    def __init__(self):
        PyQt5.QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)
        
        self.meineListe = []
        #belegen der buttons
        self.anzeigenpushButton.clicked.connect(self.klickAufAnzeigen)
        self.hinzufuegenpushButton.clicked.connect(self.klickAufHinzufuegen)
        self.hinzufuegenpushButton.hide()
        self.aenderungenSpeichernpushButton.clicked.connect(self.aenderungenSpeichern)
        self.hinzufuegenAbbrechenpushButton.clicked.connect(self.klickAufHinzufuegenAbbrechen)
        self.hinzufuegenAbbrechenpushButton.hide()
        self.aenderungenSpeichernpushButton.clicked.connect(self.aenderungenSpeichern)
        
        
        #versuche ein vorhandenes adressbuch zu oeffnen
        try:
            self.listeLaden()
            
            
        except:
            #print("except")
            #self.hinzufuegenpushButton.show()
            
            self.klickAufNeu()
            
        
    
    
    
        
    def klickAufNeu(self):
        #alle felder werden geleert, der nutzer kann einen neuen eintrag anlegen und anschliessend auf hinzufuegen klicken
        self.vornamelineEdit.setText("") #alternativ mit clear()
        self.nachnamelineEdit.setText("")
        self.emaillineEdit.setText("")
        self.handylineEdit.setText("")
        self.tellineEdit.setText("")
        self.geburtstagdateEdit.setDate(QtCore.QDate.fromString("01.01.2000", "dd.MM.yyyy"))
        self.adressetextEdit.setText("")
        self.notizentextEdit.setText("")
        self.hinzufuegenpushButton.show()
        self.aenderungenSpeichernpushButton.hide()
        self.auswahlcomboBox.hide()
        self.anzeigenpushButton.hide()
        self.hinzufuegenAbbrechenpushButton.show()
        
        
    def klickAufHinzufuegen(self):
        #beim klick auf hinzufuegen werden alle eingegebenen werte eingelesen, in eine liste gepackt, und diese in die grosse liste gepackt
        #werte einlesen
        vn = self.vornamelineEdit.text()
        nn = self.nachnamelineEdit.text()
        em = self.emaillineEdit.text()
        hn = self.handylineEdit.text()
        tn = self.tellineEdit.text()
        bday = self.geburtstagdateEdit.date().toString("dd.MM.yyyy")
        ad = self.adressetextEdit.toPlainText()
        nz = self.notizentextEdit.toPlainText()
        #werte in eine temporaere liste packen
        tempListe = [vn, nn, em, hn, tn, bday, ad, nz]
        #die temporaere liste als element der ganzen liste hinzufuegen
        self.meineListe.append(tempListe)
        #der comcobox den nachnamen hinzufuegen
        self.auswahlcomboBox.addItem(tempListe[1])
        self.statusbar.showMessage(tempListe[1] + " wurde hinzugef\u00fcgt", 3000)
        #hinzufuegen button verstecken
        self.hinzufuegenpushButton.hide()
        self.aenderungenSpeichernpushButton.show()
        self.hinzufuegenAbbrechenpushButton.hide()
        self.aenderungenSpeichernpushButton.show()
        self.auswahlcomboBox.show()
        self.anzeigenpushButton.show()
        self.klickAufAnzeigen()
        
    def listeSpeichern(self):
        #meineListe speichern auf der festplatte
        self.fobj = open("mL.pkl", "bw")
        pickle.dump(self.meineListe, self.fobj)
        self.fobj.close()
        self.statusbar.showMessage("Adressbuch wurde gespeichert", 3000)
        
        
        
    def klickAufLoeschen(self):
        #loeschen eines eintrags aus der liste
        indexderauswahl = self.auswahlcomboBox.currentIndex()
        #sicherheitsabfrage
        button = QMessageBox.question(self, "L\u00f6schen best\u00e4tigen", "Sicher dass du \"%s\" l\u00f6schen m\u00f6chtest? " % self.meineListe[indexderauswahl][1], QMessageBox.Yes | QMessageBox.No)
        if button == QMessageBox.No:
            return
        
        #element aus der combobox entfernnen
        
        self.auswahlcomboBox.removeItem(indexderauswahl)
        #elemente aus der liste entfernnen
        unnuetz = self.meineListe.pop(indexderauswahl)
        #print(self.meineListe)
        self.klickAufAnzeigen()
        self.statusbar.showMessage(unnuetz[1] + " wurde gel\u00f6scht", 3000)
        
    def klickAufAnzeigen(self):
        #der klick auf anzeigen zeigt die daten des im linken bereichs ausgewaehlten nachnamens an
        indexderauswahl = self.auswahlcomboBox.currentIndex()
        self.vornamelineEdit.setText(self.meineListe[indexderauswahl][0])
        self.nachnamelineEdit.setText(self.meineListe[indexderauswahl][1])
        self.emaillineEdit.setText(self.meineListe[indexderauswahl][2])
        self.handylineEdit.setText(self.meineListe[indexderauswahl][3])
        self.tellineEdit.setText(self.meineListe[indexderauswahl][4])
        self.geburtstagdateEdit.setDate(QtCore.QDate.fromString(self.meineListe[indexderauswahl][5], "dd.MM.yyyy"))
        self.adressetextEdit.setText(self.meineListe[indexderauswahl][6])
        self.notizentextEdit.setText(self.meineListe[indexderauswahl][7])
        
        
    def listeLaden(self):
        #eine bereits vorhandene liste(adressbuch) wird von der festplatte geladen
        #liste leeren
        self.auswahlcomboBox.clear()
        #liste laden
        self.fobj = open("mL.pkl", "rb")
        self.meineListe = pickle.load(self.fobj)
        self.fobj.close()
        #print(self.meineListe)
        for i in range(len(self.meineListe)):
            self.auswahlcomboBox.addItem(self.meineListe[i][1])
        self.klickAufAnzeigen()
        self.statusbar.showMessage("Vorhandenes Adressbuch geladen", 3000)
        
    def aenderungenSpeichern(self):
        #ein klick auf aenderungen speichern bewirkt, dass alle getaetigten aenderungen in den feldern in die liste uebernommen wird
        #es speichert aber NICHT die liste auf der festplatte
        indexderauswahl = self.auswahlcomboBox.currentIndex()
        vn = self.vornamelineEdit.text()
        nn = self.nachnamelineEdit.text()
        em = self.emaillineEdit.text()
        hn = self.handylineEdit.text()
        tn = self.tellineEdit.text()
        bday = self.geburtstagdateEdit.date().toString("dd.MM.yyyy")
        ad = self.adressetextEdit.toPlainText()
        nz = self.notizentextEdit.toPlainText()
        #werte in eine temporaere liste packen
        tempListe = [vn, nn, em, hn, tn, bday, ad, nz]
        #meine Liste umschreiben
        self.meineListe[indexderauswahl] = tempListe
        #texteintrtag in der combobox aendern
        self.auswahlcomboBox.setItemText(indexderauswahl, tempListe[1])
        
        '''  Bestaetigung fuers aendern von namen etc
        meineBox = QtWidgets.QMessageBox()
        meineBox.setIcon(QtWidgets.QMessageBox.Information)
        meineBox.setWindowTitle("\u00dcbernommen")
        meineBox.setText("\u00c4nderungen wurden \u00fcbernommen")
        meineBox.addButton(QtWidgets.QPushButton("Ok"), QtWidgets.QMessageBox.YesRole)
        hm = meineBox.exec_()
        '''
        self.statusbar.showMessage("\u00c4nderungen wurden \u00fcbernommen", 3000)
    
    def klickAufHinzufuegenAbbrechen(self):
        #bricht das hinzufuegen eines neuen adressbucheintrags ab
        self.hinzufuegenpushButton.hide()
        self.aenderungenSpeichernpushButton.show()
        self.auswahlcomboBox.show()
        self.anzeigenpushButton.show()
        self.hinzufuegenAbbrechenpushButton.hide()
        self.klickAufAnzeigen()
        
        
    def closeEvent(self, evnt): #*args, **kwargs
        #wird beim beenden des programms ausgefuehrt
        
        ''' Versuch eine eigene Box zu kreieren, klappt bis auf die ergebnisrueckgabe
        meineBox = QtWidgets.QMessageBox()
        meineBox.setIcon(QtWidgets.QMessageBox.Question)
        meineBox.setWindowTitle("Speichern?")
        meineBox.setText("Vor dem Beenden speichern?")
        meineBox.addButton(QtWidgets.QPushButton("Speichern"), QtWidgets.QMessageBox.YesRole)
        meineBox.addButton(QtWidgets.QPushButton("Beenden"), QtWidgets.QMessageBox.NoRole)
        meineBox.addButton(QtWidgets.QPushButton("Abbrechen"), QtWidgets.QMessageBox.ApplyRole)
        ret = meineBox.exec_()
        '''
        
        
        button = QMessageBox.question(self, "Speichern?", "Speichern vor dem Beenden?", QMessageBox.Save | QMessageBox.No | QMessageBox.Abort)
        
        if button == QMessageBox.Save:
            #print("Yes")
            self.listeSpeichern()
        if button == QMessageBox.No:
            #print("No")
            pass
        if button == QMessageBox.Abort:
            #print("Abort")
            evnt.ignore()
        
        
        
        #return PyQt5.QtWidgets.QMainWindow.closeEvent(self, *args, **kwargs)
        
        

        

        

app = PyQt5.QtWidgets.QApplication(sys.argv)
fenster = MeinFenster()
fenster.show()
sys.exit(app.exec_())