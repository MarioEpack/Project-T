from PyQt4 import QtCore, QtGui
import sys
import requests
import re
from pathlib import Path
from bs4 import BeautifulSoup

#### GUI modules
import design 
from login import Ui_Dialog
####

nameT, serverT, passwordT = 0, 0, 0

class MainApp(QtGui.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self) 

        dlg = StartLogin()  # Open login form before GUI is shown
        if dlg.exec_():     # Load data into global variables
            values = dlg.getValues()
            global nameT, serverT, passwordT 
            nameT = values['name']
            serverT = values['server']
            passwordT = values['password']

class StartLogin(QtGui.QDialog, Ui_Dialog):
    def __init__(self,parent=None):
        QtGui.QDialog.__init__(self,parent)
        self.setupUi(self)
        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

    def getValues(self): # Get values from login form
        return {'server': self.comboBox.currentText(), 
                'name': self.lineEdit.text(), 
                'password': self.lineEdit_2.text()}

def main():
    app = QtGui.QApplication(sys.argv)  # A new instance of QApplication
    form = MainApp()                    # We set the form to be our ExampleApp (design)
    form.show()                         # Show the form
    app.exec_()                         # and execute the app


if __name__ == '__main__':              # if we're running file directly and not importing it
    main()                              # run the main function
