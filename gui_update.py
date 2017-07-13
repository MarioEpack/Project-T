import sqlite3
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s
#This file is updating GUI via the sqlite database

def ui_update(update):
    conn = sqlite3.connect('travdate.sqlite')
    cursor = conn.cursor()
    village_id = 1
    cursor.execute('''SELECT lumber, clay, iron, crop, lumber_prod, clay_prod, iron_prod, crop_prod FROM resources WHERE village_id=?''', (village_id,))
    resources = cursor.fetchone()
    cursor.execute('''SELECT warehouse, granary  FROM storage WHERE village_id=?''', (village_id,))
    storage = cursor.fetchone()

    update.lbl_header.setText("Current / Max / Production")
    update.lbl_lumber.setText("Lumber: {0} / {1}  / {2}".format(resources[0], storage[0], resources[4]))
    update.lbl_clay.setText("Clay: {0} / {1}  / {2}".format(resources[1], storage[0], resources[5]))
    update.lbl_iron.setText("Iron: {0} / {1}  / {2}".format(resources[2], storage[0], resources[6]))
    update.lbl_crop.setText("Crop: {0} / {1}  / {2}".format(resources[3], storage[1], resources[6]))

def all_buttons(update):
    obj_button = [update.btn_id1, update.btn_id2, update.btn_id3, 
                 update.btn_id4, update.btn_id5, update.btn_id6,
                 update.btn_id7, update.btn_id8, update.btn_id9, 
                 update.btn_id10, update.btn_id11, update.btn_id12,
                 update.btn_id13, update.btn_id14, update.btn_id15, 
                 update.btn_id16, update.btn_id17, update.btn_id18,
                 update.btn_id19, update.btn_id20, update.btn_id21, 
                 update.btn_id22, update.btn_id23, update.btn_id24,
                 update.btn_id25, update.btn_id26, update.btn_id27, 
                 update.btn_id28, update.btn_id29, update.btn_id30,
                 update.btn_id31, update.btn_id32, update.btn_id33, 
                 update.btn_id34, update.btn_id35, update.btn_id36,
                 update.btn_id37, update.btn_id38]

    return obj_button


def buildings_update(update):

    conn = sqlite3.connect('travdate.sqlite')
    cur = conn.cursor()
    village_id = 1
    cur.execute('''SELECT gid, name FROM buildings''')
    data = cur.fetchall()

    buildings_list = []

    for row in data:
        buildings_list.append(row[1].encode('ascii', 'ignore'))
    
    cur.execute('''SELECT id, gid, level FROM spots WHERE village_id=?''', (village_id,))    
    data = cur.fetchall()

    obj_icon = [update.lbl_id1_icon, update.lbl_id2_icon, update.lbl_id3_icon, 
                update.lbl_id4_icon, update.lbl_id5_icon, update.lbl_id6_icon,
                update.lbl_id7_icon, update.lbl_id8_icon, update.lbl_id9_icon, 
                update.lbl_id10_icon, update.lbl_id11_icon, update.lbl_id12_icon,
                update.lbl_id13_icon, update.lbl_id14_icon, update.lbl_id15_icon, 
                update.lbl_id16_icon, update.lbl_id17_icon, update.lbl_id18_icon,
                update.lbl_id19_icon, update.lbl_id20_icon, update.lbl_id21_icon, 
                update.lbl_id22_icon, update.lbl_id23_icon, update.lbl_id24_icon,
                update.lbl_id25_icon, update.lbl_id26_icon, update.lbl_id27_icon, 
                update.lbl_id28_icon, update.lbl_id29_icon, update.lbl_id30_icon,
                update.lbl_id31_icon, update.lbl_id32_icon, update.lbl_id33_icon, 
                update.lbl_id34_icon, update.lbl_id35_icon, update.lbl_id36_icon,
                update.lbl_id37_icon, update.lbl_id38_icon]

    obj_text = [update.lbl_id1, update.lbl_id2, update.lbl_id3, 
                update.lbl_id4, update.lbl_id5, update.lbl_id6,
                update.lbl_id7, update.lbl_id8, update.lbl_id9, 
                update.lbl_id10, update.lbl_id11, update.lbl_id12,
                update.lbl_id13, update.lbl_id14, update.lbl_id15, 
                update.lbl_id16, update.lbl_id17, update.lbl_id18,
                update.lbl_id19, update.lbl_id20, update.lbl_id21, 
                update.lbl_id22, update.lbl_id23, update.lbl_id24,
                update.lbl_id25, update.lbl_id26, update.lbl_id27, 
                update.lbl_id28, update.lbl_id29, update.lbl_id30,
                update.lbl_id31, update.lbl_id32, update.lbl_id33, 
                update.lbl_id34, update.lbl_id35, update.lbl_id36,
                update.lbl_id37, update.lbl_id38]

    for building in data:
        if building[1] == 0:
            name = buildings_list[0]
            obj_text[building[0]-1].setText(name)
            icon = QtGui.QPixmap(_fromUtf8("images/buildings/g0.gif"))
            icon = icon.scaled(40, 40, QtCore.Qt.KeepAspectRatio)
            obj_icon[building[0]-1].setPixmap(icon)
        else:
            name = str(buildings_list[building[1]]) + " " + str(building[2])
            obj_text[building[0]-1].setText(name)
            icon = QtGui.QPixmap(_fromUtf8("images/buildings/g{0}.gif".format(building[1])))
            icon = icon.scaled(40, 40, QtCore.Qt.KeepAspectRatio)
            obj_icon[building[0]-1].setPixmap(icon)