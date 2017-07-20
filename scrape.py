import re
from bs4 import BeautifulSoup
import sqlite3
import requests

#Scraping the updates
#UPDATE STORAGE FUNCTIONS

def update_lumber_stock(my_soup):
    lumber_storage = my_soup.find(id= "l1")
    value_re = re.findall(r'\d', str(lumber_storage))
    value_re.remove(value_re[0])
    value = ''.join(value_re)
    return value

def update_clay_stock(my_soup):
    clay_storage = my_soup.find(id= "l2")
    value_re = re.findall(r'\d', str(clay_storage))
    value_re.remove(value_re[0])
    value = ''.join(value_re)
    return value

def update_iron_stock(my_soup):
    iron_storage = my_soup.find(id= "l3")
    value_re = re.findall(r'\d', str(iron_storage))
    value_re.remove(value_re[0])
    value = ''.join(value_re)
    return value

def update_crop_stock(my_soup):
    crop_storage = my_soup.find(id= "l4")
    value_re = re.findall(r'\d', str(crop_storage))
    value_re.remove(value_re[0])
    value = ''.join(value_re)
    return value

def update_warehouse(my_soup):
    warehouse_storage = my_soup.find(id="stockBarWarehouse")
    value_re = re.findall(r'\d', str(warehouse_storage))
    value = ''.join(value_re)
    return value

def update_granary(my_soup):
    granary_storage = my_soup.find(id="stockBarGranary")
    value_re = re.findall(r'\d', str(granary_storage))
    value = ''.join(value_re)
    return value

#UPDATE PRODUCTION FUNCTIONS       

def update_lumber_prod(my_soup):
    soup_lumber_prod = my_soup.find(href="production.php?t=1")
    lumber_prod = re.findall(r'\d+', str(soup_lumber_prod))
    return lumber_prod[1]
    
def update_clay_prod(my_soup):
    soup_clay_prod = my_soup.find(href="production.php?t=2")
    clay_prod = re.findall(r'\d+', str(soup_clay_prod))
    return clay_prod[1]

def update_iron_prod(my_soup):
    soup_iron_prod = my_soup.find(href="production.php?t=3")
    iron_prod = re.findall(r'\d+', str(soup_iron_prod))
    return iron_prod[1]

def update_crop_prod(my_soup):
    soup_crop_prod = my_soup.find(href="production.php?t=5")
    crop_prod = re.findall(r'\d+', str(soup_crop_prod))
    return crop_prod[3]

def total_update():
    print update_lumber_stock(my_soup)
    print update_crop_stock(my_soup)
    print update_iron_stock(my_soup)
    print update_clay_stock(my_soup)
    print update_warehouse(my_soup)
    print update_granary(my_soup)

    print update_lumber_prod(my_soup)
    print update_clay_prod(my_soup)
    print update_iron_prod(my_soup)
    print update_crop_prod(my_soup)

#UPDATE BUILDINGS FUNCTIONS

def get_spot_info(session):
    value = []
    for x in range(1, 39):

        html = session.get("http://ts2.travian.sk/build.php?id= %d" % (x))
        unicodeData = html.text
        unicodeData.encode('ascii', 'ignore')
        soup = BeautifulSoup(unicodeData, 'html.parser')
        scrape = soup.find(id="build")
        spot = re.findall(r'\d+', str(scrape))
        if spot[0] == "0":
            spot[1] = 0
        triple_tup = ("1", x, spot[0], spot[1])
        value.append(triple_tup)

    return value

def create_buildings_list():
    value = []
    for x in range(0,42):

        name = ["Empty field","Woodcutter","Clay Pit","Iron Mine","Cropland","Sawmill",
                "Brickyard","Iron Foundry","Grain Mill","Bakery","Warehouse",
                "Granary", "0", "Smithy","Tournament Square","Main Building","Rally Point",
                "Marketplace","Embassy","Barracks","Stable","Workshop",
                "Academy","Cranny","Town Hall","Residence","Palace",
                "Treasury","Trade Office","Great Barracks","Great Stable",
                "City Wall","Earth Wall","Palisade","Stonemason's Lodge","Brewery",
                "Trapper","Hero's Mansion","Great Warehouse","Great Granary",
                "Wonder of the World","Horse Drinking Trough"]
        triple_tup = (x, name[x], 0, 0, 0)
        value.append(triple_tup)

    return value


#SQLITE execute


def sqlite_update(session):
    
    html = session.get('http://ts2.travian.sk/dorf1.php')
    unicodeData = html.text
    unicodeData.encode('ascii', 'ignore')
    my_soup = BeautifulSoup(unicodeData, 'html.parser')

    #SQLITE code
    conn = sqlite3.connect('travdate.sqlite')
    cur = conn.cursor()

    cur.executescript('''
    DROP TABLE IF EXISTS resources;
    DROP TABLE IF EXISTS storage;
    DROP TABLE IF EXISTS spots;
    DROP TABLE IF EXISTS buildings;

    CREATE TABLE resources (
        village_id   INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        lumber       INTEGER NOT NULL,
        clay         INTEGER NOT NULL,
        iron         INTEGER NOT NULL,
        crop         INTEGER NOT NULL,
        lumber_prod  INTEGER NOT NULL,
        clay_prod    INTEGER NOT NULL,
        iron_prod    INTEGER NOT NULL,
        crop_prod    INTEGER NOT NULL
    );

    CREATE TABLE storage (
        village_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        warehouse   INTEGER NOT NULL,
        granary    INTEGER NOT NULL

    );

    CREATE TABLE spots (
        village_id INTEGER NOT NULL,
        id INTEGER NOT NULL,
        gid   INTEGER NOT NULL,
        level   INTEGER NOT NULL

    );

    CREATE TABLE buildings ( 
        gid INTEGER NOT NULL PRIMARY KEY UNIQUE,
        name TEXT NOT NULL, 
        req1 INTEGER NOT NULL, 
        req2 INTEGER NOT NULL, 
        req3 INTEGER NOT NULL
    )
    ''')

    cur.execute('''INSERT INTO resources(lumber, clay, iron, crop, lumber_prod,
    clay_prod, iron_prod, crop_prod) VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
    (update_lumber_stock(my_soup), update_clay_stock(my_soup), update_iron_stock(my_soup), 
        update_crop_stock(my_soup), update_lumber_prod(my_soup),update_clay_prod(my_soup),
        update_iron_prod(my_soup), update_crop_prod(my_soup)))

    cur.execute('''INSERT INTO storage(warehouse, granary) VALUES(?, ?)''',
        (update_warehouse(my_soup), update_granary(my_soup)))

    values_to_insert = get_spot_info(session)

    cur.executemany('''
        INSERT INTO spots ('village_id','id', 'gid', 'level')
        VALUES (?, ?, ?, ?)''', values_to_insert) 

    values_to_insert = create_buildings_list()

    cur.executemany('''
        INSERT INTO buildings ('gid', 'name', 'req1', 'req2', 'req3')
        VALUES (?, ?, ?, ?, ?)''', values_to_insert)
    
    conn.commit()

def upgrade_link(session, building_id):

    html = session.get("http://ts2.travian.sk/build.php?id=%d" % (building_id))
    unicodeData = html.text
    soup = BeautifulSoup(unicodeData, 'html.parser')

    my_re = re.findall(r'dorf..php\?a=...............', str(soup))
    re_str = my_re[0]
    re_list = list(re_str)
    re_list.pop(15)
    re_list.pop(15)
    re_list.pop(15)
    re_list.pop(15)
    re_str = "".join(re_list)
    return re_str

def is_building(village_id=1):
    # This function inserts build_info into sqlite, or returns False
   
    try:
        #SQLITE code
        conn = sqlite3.connect('travdate.sqlite')
        cur = conn.cursor()
        #request and soup
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
                   'name': "Ashreen", 
                   'password': "testing", 
                   's1': 'Login', 
                   'w': '1920:1080'}


        session = requests.Session()

        session.post('http://ts2.travian.sk/dorf1.php', data=payload, cookies=r1.cookies)
        req = session.get('http://ts2.travian.sk/dorf2.php')

        unicodeData = req.text
        unicodeData.encode('ascii', 'ignore')
        soup = BeautifulSoup(unicodeData, 'html.parser')
        #Time left in seconds
        time_left = soup.find("div", {"class" : "buildDuration"})
        time_left = list(time_left)[1]
        time_left = re.findall(r"\d+", str(time_left))
        time_left = time_left[0]
        #level, gid, aid
        level_info = re.findall(r"\"stufe\":..", str(soup))[0]
        level_info = re.findall(r"\d+", level_info)[0]
        gid_info = re.findall(r"\"gid\":\"....", str(soup))[0]
        gid_info = re.findall(r"\d+", gid_info)[0]
        aid_info = re.findall(r"\"aid\":\"....", str(soup))[0]
        aid_info = re.findall(r"\d+", aid_info)[0]
        #SQL execute
        cur.executescript('''
        DROP TABLE IF EXISTS build_queue;

        CREATE TABLE build_queue (
        id         INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        village_id INTEGER NOT NULL,
        gid   INTEGER NOT NULL,
        aid    INTEGER NOT NULL,
        level  INTEGER NOT NULL,
        active INTEGER NOT NULL,
        timer INTEGER NOT NULL
        )
        ''')

        cur.execute('''INSERT INTO build_queue(village_id, gid, aid, level, active, timer)
        VALUES(?, ?, ?, ?, ?, ?)''',
        (village_id, gid_info, aid_info, level_info, "1", time_left))
        conn.commit()
        return True
    except TypeError:    
        return False



