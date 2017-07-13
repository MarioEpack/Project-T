from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QThread, SIGNAL
import sys
import requests
import re
from pathlib import Path
from bs4 import BeautifulSoup

#### GUI modules
import design 
from login import Ui_Dialog
#### Processing modules
from gui_update import *
from scrape import *


loginDetails = {}

class UpdateTab1(QThread):

    def __init__(self, myvar, parent=None):
        QThread.__init__(self)
        self.myvar = myvar

    def __del__(self):
        self.wait()

    def getCookies(self):
        global loginDetails
        r1 = requests.get('http://ts2.travian.sk/login.php')
        unicodeData = r1.text
        unicodeData.encode('ascii', 'ignore')
        soup = BeautifulSoup(unicodeData, 'html.parser')
        tags = soup('input')
        value_list = []

        for tag in tags:
            value_list.append(tag.get('value', None))

        my_id = value_list[4]

        payload = {'login': my_id, 
                   'name': str(loginDetails["name"]), 
                   'password': str(loginDetails["password"]), 
                   's1': 'Login', 
                   'w': '1920:1080'}


        session = requests.Session()

        session.post('http://ts2.travian.sk/dorf1.php', data=payload, cookies=r1.cookies)
        return session

    def run(self): 
        if self.myvar == 'a':
            #sqlite_update(self.getCookies())
            self.emit(SIGNAL('change_label(QString)'), loginDetails["name"])
        elif self.myvar == 'b':
            """session = self.getCookies()
            link = upgrade_link(session, 21)
            session.get('http://ts2.travian.sk/{0}'.format(link))
            self.emit(SIGNAL('change_label(QString)'), loginDetails["name"]) """    

class MainApp(QtGui.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self) 

        self.hide_buttons_and_connect_all()
        global loginDetails
        dlg = StartLogin()  # Open login form before GUI is shown
        if dlg.exec_():     # Load data into global variables
            values = dlg.getValues()
            loginDetails['name'] = values['name']
            loginDetails['password'] = values['password']
        else:
            loginDetails['name'] = "Ashreen"
            loginDetails['password'] = "testing"

        self.start_update_tab1()
        self.btn_update.clicked.connect(self.start_update_tab1)
        

    def start_update_tab1(self):
        self.get_thread = UpdateTab1(myvar="a")
        self.connect(self.get_thread, SIGNAL("change_label(QString)"), self.change_label)
        self.connect(self.get_thread, SIGNAL("finished()"), self.done)
        self.get_thread.start()
        self.btn_update.setEnabled(False)
        self.btn_update.setText("Updating")

    def upgrade_building(self, ids):
        print ids
        self.get_thread = UpdateTab1(myvar="b")
        self.connect(self.get_thread, SIGNAL("finished()"), lambda: self.doneUpgrade(ids))
        self.get_thread.start()
        #self.btn_up_id1.setEnabled(False)
        #button.setText("Adding")

    def change_label(self, text):
        self.label.setText(text)

    def done(self):
        self.btn_update.setEnabled(True)
        QtGui.QMessageBox.information(self, "Done!", "Done fetching data!")
        ui_update(self)
        buildings_update(self)

    def hide_buttons_and_connect_all(self):
        buttons = all_buttons(self)
        i = 0
        for btn in buttons:
            #btn.hide()
            btn.setText(str(i))
            btn.clicked.connect(lambda: self.upgrade_building(i))
            i += 1

    def doneUpgrade(self, ids):
        buttons = all_buttons(self)
        buttons[ids].setText("cas")
        QtGui.QMessageBox.information(self, "Upgrade building", "Upgrade for building was added to queue!")


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