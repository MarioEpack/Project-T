# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design_login.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(300, 170)
        self.le_name = QtGui.QLineEdit(Dialog)
        self.le_name.setGeometry(QtCore.QRect(75, 60, 150, 20))
        self.le_name.setObjectName(_fromUtf8("le_name"))
        self.le_password = QtGui.QLineEdit(Dialog)
        self.le_password.setGeometry(QtCore.QRect(75, 90, 150, 20))
        self.le_password.setObjectName(_fromUtf8("le_password"))
        self.cb_server = QtGui.QComboBox(Dialog)
        self.cb_server.setGeometry(QtCore.QRect(100, 30, 100, 22))
        self.cb_server.setObjectName(_fromUtf8("cb_server"))
        self.cb_server.addItem(_fromUtf8(""))
        self.cb_server.addItem(_fromUtf8(""))
        self.btn_continue = QtGui.QPushButton(Dialog)
        self.btn_continue.setEnabled(False)
        self.btn_continue.setGeometry(QtCore.QRect(155, 120, 70, 20))
        self.btn_continue.setObjectName(_fromUtf8("btn_continue"))
        self.btn_login = QtGui.QPushButton(Dialog)
        self.btn_login.setGeometry(QtCore.QRect(75, 120, 70, 20))
        self.btn_login.setObjectName(_fromUtf8("btn_login"))
        self.lbl_login_info = QtGui.QLabel(Dialog)
        self.lbl_login_info.setGeometry(QtCore.QRect(10, 10, 280, 16))
        self.lbl_login_info.setObjectName(_fromUtf8("lbl_login_info"))
        self.lb_login_status = QtGui.QLabel(Dialog)
        self.lb_login_status.setGeometry(QtCore.QRect(10, 150, 280, 13))
        self.lb_login_status.setText(_fromUtf8(""))
        self.lb_login_status.setObjectName(_fromUtf8("lb_login_status"))

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.btn_continue, QtCore.SIGNAL(_fromUtf8("clicked(bool)")), Dialog.accept)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.cb_server.setItemText(0, _translate("Dialog", "ts3.travian.sk", None))
        self.cb_server.setItemText(1, _translate("Dialog", "ts2.travian.sk", None))
        self.btn_continue.setText(_translate("Dialog", "Continue", None))
        self.btn_login.setText(_translate("Dialog", "Login", None))
        self.lbl_login_info.setText(_translate("Dialog", "Enter your login details:", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

