import sqlite3
#This file is updating GUI via the sqlite database

def ui_update(update):


    conn = sqlite3.connect('travdate.sqlite')
    cur = conn.cursor()

    village_id = 1
    cur.execute('''SELECT * FROM resources WHERE village_id=?''', (village_id,))
    data = cur.fetchone()
    
    lumber = data[1], clay = data[2], iron = data[3], crop = data[4]
    lumber_prod = data[5], clay_prod = data[6], iron_prod = data[7]
    crop_prod = data[8]

    cur.execute('''SELECT * FROM storage WHERE village_id=?''', (village_id))
    data = cur.fetchone()
    warehouse = data[1], grannary = data[2]

    update.lbl_header.setText("Current / Max / Production")
    update.lbl_lumber.setText("Lumber: {1} / {2} / {3}").format(lumber, warehouse, lumber_prod)
    update.lbl_clay.setText("Clay: {1} / {2} / {3}").format(clay, warehouse, clay_prod)
    update.lbl_iron.setText("Iron: {1} / {2} / {3}").format(iron, warehouse, iron_prod)
    update.lbl_crop.setText("Crop: {1} / {2} / {3}").format(crop, granary, crop_prod)
