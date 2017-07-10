import sqlite3
#This file is updating GUI via the sqlite database info

def Ui_update(update):

    conn.execute("SELECT warehouse FROM storage")
    storage = conn.fetchone()

    def header_update(update):
        update.label_header.setText("Current / Max / Production")

    def lumber_update(update):
        update.label_lumber.setText("Lumber: {1} / {2}  / {3}").format(lumber, warehouse, lumber_prod)
        conn.execute("SELECT lumber FROM resources")
        lumber = conn.fetchone()
        conn.execute("SELECT lumber_prod FROM resources")
        lumber_prod = conn.fetchone()

    def crop_update(update):
        update.label_crop.setText("Crop: {1} / {2}  / {3}").format(crop, warehouse, crop_prod)
        conn.execute("SELECT crop FROM resources")
        crop = conn.fetchone()
        conn.execute("SELECT crop_prod FROM resources")
        crop_prod = conn.fetchone()

    def iron_update(update):
        update.label_iron.setText("Iron: {1} / {2}  / {3}").format(iron, warehouse, iron_prod)
        conn.execute("SELECT iron FROM resources")
        iron = conn.fetchone()
        conn.execute("SELECT iron_prod FROM resources")
        iron_prod = conn.fetchone()

    def clay_update(update):
        update.label_clay.setText("Clay: {1} / {2}  / {3}").format(clay, warehouse, clay_prod)
        conn.execute("SELECT clay FROM resources")
        clay = conn.fetchone()
        conn.execute("SELECT clay_prod FROM resources")
        clay_prod = conn.fetchone()


conn = sqlite3.connect('travdate.sqlite')
cur = conn.cursor()
Ui_update(update)
conn.commit()

