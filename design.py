# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design.ui'
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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(800, 600)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 60, 801, 511))
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.lbl_lumber = QtGui.QLabel(self.tab)
        self.lbl_lumber.setGeometry(QtCore.QRect(50, 40, 250, 20))
        self.lbl_lumber.setObjectName(_fromUtf8("lbl_lumber"))
        self.label_2 = QtGui.QLabel(self.tab)
        self.label_2.setGeometry(QtCore.QRect(360, 250, 46, 13))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.btn_update = QtGui.QPushButton(self.tab)
        self.btn_update.setGeometry(QtCore.QRect(610, 450, 75, 23))
        self.btn_update.setObjectName(_fromUtf8("btn_update"))
        self.lbl_icon_lumber = QtGui.QLabel(self.tab)
        self.lbl_icon_lumber.setGeometry(QtCore.QRect(20, 40, 20, 20))
        self.lbl_icon_lumber.setText(_fromUtf8(""))
        self.lbl_icon_lumber.setPixmap(QtGui.QPixmap(_fromUtf8("images/lumber_small.png")))
        self.lbl_icon_lumber.setObjectName(_fromUtf8("lbl_icon_lumber"))
        self.lbl_header = QtGui.QLabel(self.tab)
        self.lbl_header.setGeometry(QtCore.QRect(20, 20, 200, 20))
        self.lbl_header.setText(_fromUtf8(""))
        self.lbl_header.setObjectName(_fromUtf8("lbl_header"))
        self.lbl_icon_clay = QtGui.QLabel(self.tab)
        self.lbl_icon_clay.setGeometry(QtCore.QRect(20, 60, 20, 20))
        self.lbl_icon_clay.setText(_fromUtf8(""))
        self.lbl_icon_clay.setPixmap(QtGui.QPixmap(_fromUtf8("images/clay_small.png")))
        self.lbl_icon_clay.setObjectName(_fromUtf8("lbl_icon_clay"))
        self.label = QtGui.QLabel(self.tab)
        self.label.setGeometry(QtCore.QRect(290, 330, 46, 13))
        self.label.setObjectName(_fromUtf8("label"))
        self.lbl_icon_iron = QtGui.QLabel(self.tab)
        self.lbl_icon_iron.setGeometry(QtCore.QRect(20, 80, 20, 20))
        self.lbl_icon_iron.setText(_fromUtf8(""))
        self.lbl_icon_iron.setPixmap(QtGui.QPixmap(_fromUtf8("images/iron_small.png")))
        self.lbl_icon_iron.setObjectName(_fromUtf8("lbl_icon_iron"))
        self.lbl_icon_crop = QtGui.QLabel(self.tab)
        self.lbl_icon_crop.setGeometry(QtCore.QRect(20, 100, 20, 20))
        self.lbl_icon_crop.setText(_fromUtf8(""))
        self.lbl_icon_crop.setPixmap(QtGui.QPixmap(_fromUtf8("images/oasis_small.png")))
        self.lbl_icon_crop.setObjectName(_fromUtf8("lbl_icon_crop"))
        self.lbl_clay = QtGui.QLabel(self.tab)
        self.lbl_clay.setGeometry(QtCore.QRect(50, 60, 250, 20))
        self.lbl_clay.setObjectName(_fromUtf8("lbl_clay"))
        self.lbl_iron = QtGui.QLabel(self.tab)
        self.lbl_iron.setGeometry(QtCore.QRect(50, 80, 250, 20))
        self.lbl_iron.setObjectName(_fromUtf8("lbl_iron"))
        self.lbl_crop = QtGui.QLabel(self.tab)
        self.lbl_crop.setGeometry(QtCore.QRect(50, 100, 250, 20))
        self.lbl_crop.setObjectName(_fromUtf8("lbl_crop"))
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Project T", None))
        self.lbl_lumber.setText(_translate("MainWindow", "0/0/0", None))
        self.label_2.setText(_translate("MainWindow", "TextLabel", None))
        self.btn_update.setText(_translate("MainWindow", "Update", None))
        self.label.setText(_translate("MainWindow", "TextLabel", None))
        self.lbl_clay.setText(_translate("MainWindow", "0/0/0", None))
        self.lbl_iron.setText(_translate("MainWindow", "0/0/0", None))
        self.lbl_crop.setText(_translate("MainWindow", "0/0/0", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Tab 1", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Tab 2", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

