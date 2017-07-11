import sqlite3
#This file is updating GUI via the sqlite database

def ui_update(update):

    conn = sqlite3.connect('travdate.sqlite')
    cur = conn.cursor()

    village_id = 1
    cur.execute('''SELECT * FROM resources WHERE village_id=?''', (village_id,))
    data = cur.fetchone()
    
    lumber = data[1]; clay = data[2]; iron = data[3]; crop = data[4]
    lumber_prod = data[5]; clay_prod = data[6]; iron_prod = data[7]
    crop_prod = data[8]

    cur.execute('''SELECT * FROM storage WHERE village_id=?''', (village_id,))
    data = cur.fetchone()
    warehouse = data[1]; grannary = data[2]

    lumber_txt = "Lumber: %s / %s / %s" % (lumber, warehouse, lumber_prod)
    clay_txt = "Clay: %s / %s / %s" % (clay, warehouse, clay_prod)
    iron_txt = "Iron: %s / %s / %s" % (iron, warehouse, iron_prod)
    crop_txt = "Crop: %s / %s / %s" % (crop, grannary, crop_prod)

    update.lbl_header.setText("Current / Max / Production")
    update.lbl_lumber.setText(lumber_txt)
    update.lbl_clay.setText(clay_txt)
    update.lbl_iron.setText(iron_txt)
    update.lbl_crop.setText(crop_txt)


def buildings_update(update):

    conn = sqlite3.connect('travdate.sqlite')
    cur = conn.cursor()
    cur.execute('''SELECT name, level FROM buildings ,spots 
    WHERE spots.gid=buildings.gid''')

    data = cur.fetchall()

    for building in data:
        name = building[0].encode('ascii', 'ignore')
        level = str(building[1])
        update.lbl_id1.setText(name + " " + level)
        icon = QtGui.QPixmap(_fromUtf8("images/buildings/g(%s).gif")) % (level)
        icon = icon.scaled(40, 40, QtCore.Qt.KeepAspectRatio)
        update.lbl_id1_icon.setPixmap(icon)
