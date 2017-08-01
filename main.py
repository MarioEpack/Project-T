from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QThread, SIGNAL
import sys
import requests
import re
from pathlib import Path
from bs4 import BeautifulSoup
from time import strftime
#### GUI modules
import design 
#### Processing modules
from gui_update import *
from scrape import *
from login import *

sessionGlobal = requests.Session()
serverGlobal = ""

class Update(QThread):

    def __init__(self, myvar, parent=None):
        QThread.__init__(self)
        self.myvar = myvar

    def __del__(self):
        self.wait()      

    def run(self): 
        if self.myvar == 'a':
            sqlite_update(sessionGlobal, serverGlobal)
            #map_scan(-51, -29, 3, sessionGlobal, serverGlobal)
        elif self.myvar == 'b':
            """session = self.getCookies()
            link = upgrade_link(session, 21)
            session.get('http://ts2.travian.sk/{0}'.format(link))
            self.emit(SIGNAL('change_label(QString)'), loginDetails["name"]) """         

class MainApp(QtGui.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        #Open login form 
        #Get session if login succeeded or terminate app if form was closed
        global serverGlobal, sessionGlobal
        sessionGlobal = loginForm()
        serverGlobal = server_file(1)
        #Set timer variables
        self.time_left = 0
        self.ctimer = QtCore.QTimer()
        self.stimer = QtCore.QTimer()
        #Run initial functions
        self.hide_buttons_and_connect_all()
        self.start_update() 
        #Add connects
        self.btn_update.clicked.connect(self.start_update)
        self.pushButton.clicked.connect(self.next_building)

    def start_update(self):
        self.get_thread = Update(myvar="a")
        self.connect(self.get_thread, SIGNAL("change_label(QString)"), self.change_label)
        self.connect(self.get_thread, SIGNAL("finished()"), self.done)
        self.get_thread.start()
        self.btn_update.setEnabled(False)
        self.btn_update.setText("Updating")

    def add_building(self, ids):
        buttons = all_buttons(self)
        buttons[ids].setEnabled(False)
        buttons[ids].setText("Adding")
        btn_id = str(buttons[ids].objectName())
        btn_id = btn_id[6:]

        conn = sqlite3.connect('travdate.sqlite')
        cur = conn.cursor()
        cur.execute('''SELECT gid, level FROM spots WHERE village_id=? AND id=?''', ("1", btn_id))
        data = cur.fetchone()

        buildings_list = buildings()
        datai = data[1]+1

        cur.execute('''INSERT INTO build_queue(village_id, gid, aid, level, active, timer)
        VALUES(?, ?, ?, ?, ?, ?)''',
        (1, data[0], btn_id, str(datai), 0, 0))
        conn.commit()

        self.listWidget.addItem(buildings_list[data[0]] + " to level " + str(datai))

    def start_build_queue(self):
        conn = sqlite3.connect('travdate.sqlite')
        cursor = conn.cursor()
        village_id = 1
        buildings_list = buildings()

        if is_building(village_id, sessionGlobal, serverGlobal) == True:
            
            cursor.execute('''SELECT id, gid, aid, level, timer FROM build_queue WHERE village_id=? and active = 1''', (village_id,))
            data = cursor.fetchone()
            times = (data[4]*1000)+2000

            cursor.execute('''SELECT name FROM buildings WHERE gid=?''', (data[1],))    
            data2 = cursor.fetchone()
            print data
            print data2
            self.budova.setText(str(data2[0]) + " is being upgraded to level " + str(data[3]) + ".")

            self.ctimer.timeout.connect(self.change_timer)
            self.ctimer.start(1000) 
            self.stimer.singleShot(times, self.next_building)
            self.time_left = data[4]

            cursor.execute('''SELECT exists(SELECT 1 FROM build_queue WHERE village_id = 1 and active = 0);''')

            if data[0] == 1:
                cursor.execute('''SELECT gid, level FROM build_queue WHERE village_id=? and active = 0''', (village_id,))
                data = cursor.fetchall()

                for row in data:
                    self.listWidget.addItem(buildings_list[row[0]] + " to level " + str(row[1]))
            else:
                self.listWidget.addItem("Build queue is empty!")
        else:
            cursor.execute('''DELETE FROM build_queue WHERE village_id=? and active = 1''', (village_id,))
            conn.commit()

            cursor.execute('''SELECT exists(SELECT 1 FROM build_queue WHERE village_id = 1 and active = 0);''')
            data = cursor.fetchone()

            if data[0] == 1:
                cursor.execute('''SELECT gid, level, id, aid FROM build_queue WHERE village_id=? and active = 0''', (village_id,))
                data = cursor.fetchone()
                link = upgrade_link(sessionGlobal, serverGlobal, data[3])
                req = session.get('http://{1}/{0}'.format(link, serverGlobal))

                unicodeData = req.text
                unicodeData.encode('ascii', 'ignore')
                soup = BeautifulSoup(unicodeData, 'html.parser')
                #Time left in seconds
                time_left = soup.find("div", {"class" : "buildDuration"})
                time_left = list(time_left)[1]
                time_left = re.findall(r"\d+", str(time_left))
                time_left = time_left[0]
                times = (int(time_left)*1000)+2000

                self.ctimer.timeout.connect(self.change_timer)
                self.ctimer.start(1000) 
                self.stimer.singleShot(times, self.next_building)
                self.time_left = int(time_left)
                self.budova.setText(str(data[0]) + " is being upgraded to level " + str(data[1]) + ".")

                cursor.execute("UPDATE build_queue SET active = 1, timer = ? WHERE id = ?", (int(time_left),data[2]))
                conn.commit()

                cursor.execute('''SELECT exists(SELECT 1 FROM build_queue WHERE village_id = 1 and active = 0);''')
                data = cursor.fetchone()

                if data[0] == 0:
                    self.listWidget.addItem("Build queue is empty!")
                else:
                    cursor.execute('''SELECT gid, level FROM build_queue WHERE village_id=? and active = 0''', (village_id,))
                    data = cursor.fetchall()

                    for row in data:
                        self.listWidget.addItem(buildings_list[row[0]] + " to level " + str(row[1]))
            else:
                self.listWidget.addItem("Build queue is empty!")

    def change_label(self, text):
        self.label.setText(text)

    def change_timer(self):
        self.lcd_time_left.display(self.time_left)
        self.time_left -= 1

    def next_building(self):
        self.ctimer.stop()
        conn = sqlite3.connect('travdate.sqlite')
        cursor = conn.cursor()
        village_id = 1

        cursor.execute('''DELETE FROM build_queue WHERE village_id=? and active = 1''', (village_id,))
        conn.commit()
        cursor.execute('''SELECT gid, level, id, aid FROM build_queue WHERE village_id=? and active = 0''', (village_id,))
        data = cursor.fetchone()
        link = upgrade_link(sessionGlobal, serverGlobal, data[3])
        session.get('http://{1}/{0}'.format(link, serverGlobal))

        buildings_list = buildings()

        req = session.get('http://{0}/dorf2.php'.format(serverGlobal))

        unicodeData = req.text
        unicodeData.encode('ascii', 'ignore')
        soup = BeautifulSoup(unicodeData, 'html.parser')
        #Time left in seconds
        time_left = soup.find("div", {"class" : "buildDuration"})
        time_left = list(time_left)[1]
        time_left = re.findall(r"\d+", str(time_left))
        time_left = time_left[0]
        times = (int(time_left)*1000)+2000

        self.ctimer.timeout.connect(self.change_timer)
        self.ctimer.start(1000) 
        self.stimer.singleShot(times, self.next_building)
        self.time_left = int(time_left)
        self.budova.setText(str(data[0]) + " is being upgraded to level " + str(data[1]) + ".")

        cursor.execute("UPDATE build_queue SET active = 1, timer = ? WHERE id = ?", (int(time_left),data[2]))
        conn.commit()

        cursor.execute('''SELECT gid, level FROM build_queue WHERE village_id=? and active = 0''', (village_id,))
        data = cursor.fetchall()

        self.listWidget.clear()

        for row in data:
            self.listWidget.addItem(buildings_list[row[0]] + " to level " + str(row[1]))

    def done(self):
        self.btn_update.setEnabled(True)
        QtGui.QMessageBox.information(self, "Done!", "Done fetching data!")
        ui_update(self)
        buildings_update(self)
        self.start_build_queue()

    def hide_buttons_and_connect_all(self):
        buttons = all_buttons(self)
        helper = lambda i: (lambda: self.add_building(i))
        for i in range(0,38):
            buttons[i].hide()
            buttons[i].clicked.connect(helper(i))
            i += 1

    def doneUpgrade(self, ids):
        buttons = all_buttons(self)
        buttons[ids].setText("cas")
        QtGui.QMessageBox.information(self, "Upgrade building", "Upgrade for building {0} was added to queue!".format(ids))




def main():
    app = QtGui.QApplication(sys.argv)  # A new instance of QApplication
    form = MainApp()                    # Set the form
    form.show()                         # Show the form
    app.exec_()                         # and execute the app


if __name__ == '__main__':              # if we're running file directly and not importing it
    main()                              # run the main function