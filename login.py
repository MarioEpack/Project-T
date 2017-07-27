from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QThread, SIGNAL
import sys
import requests
import re
from bs4 import BeautifulSoup
#Load gui module
from design_login import Ui_Dialog

session = requests.Session()

class StartLogin(QtGui.QDialog, Ui_Dialog):
    def __init__(self,parent=None):
        QtGui.QDialog.__init__(self,parent)
        self.setupUi(self)
        
        self.btn_login.clicked.connect(self.getSession)

    def getValues(self): # Get values from login form
        return {'server': self.cb_server.currentText(), 
                'name': self.le_name.text(), 
                'password': self.le_password.text()}

    #Function to get session from provided login details
    def getSession(self):
        self.btn_login.setEnabled(False)
        self.lb_login_status.setStyleSheet('color: yellow')
        self.lb_login_status.setText("Login in progress! Please Wait ...")
        global session
        req = requests.get('http://{0}/login.php'.format(str(self.cb_server.currentText())))
        unicodeData = req.text
        unicodeData.encode('ascii', 'ignore')
        soup = BeautifulSoup(unicodeData, 'html.parser')
        tags = soup('input')
        value_list = []
        for tag in tags:
            value_list.append(tag.get('value', None))
        my_id = value_list[4]
        payload = {'login': my_id, 
                   'name': str(self.le_name.text()), 
                   'password': str(self.le_password.text()), 
                   's1': 'Login', 
                   'w': '1920:1080'}

        req = session.post('http://{0}/dorf1.php'.format(str(self.cb_server.currentText())), data=payload, cookies=req.cookies)
        test_str = req.text
        if test_str.find("villageNameField") == -1:
            self.btn_login.setEnabled(True)
            self.lb_login_status.setStyleSheet('color: red')
            self.lb_login_status.setText("Login failed! Check your details and try again.")
        else:
            server_file(0, str(self.cb_server.currentText()))
            self.lb_login_status.setStyleSheet('color: green')
            self.lb_login_status.setText("Login successful! Click continue to proceed.")
            self.btn_continue.setEnabled(True)

#Function for passing session to main app
def passSession():
    return session

#Function to create login form
def loginForm():
    dlg = StartLogin()  
    if dlg.exec_():     
        return passSession()
    else:
        sys.exit()

#Function to save or load server name from file
def server_file(row, data=0):
    if row == 0:
        file_name = open("server.txt", "w+")
        file_name.write(data)
        file_name.close()
    elif row == 1:
        file = open("server.txt", "r+")
        return file.read()
