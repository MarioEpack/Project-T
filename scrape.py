import re
from bs4 import BeautifulSoup
import sqlite3
import requests
import math
import decimal

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

#UPDATE BUILDINGS FUNCTIONS

def get_spot_info(session, server):
    value = []
    for x in range(1, 39):

        html = session.get("http://{0}/build.php?id={1}".format(server, x))
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

def buildings():
    conn = sqlite3.connect('travdate.sqlite')
    cursor = conn.cursor()
    cursor.execute('''SELECT gid, name FROM buildings''')
    data2 = cursor.fetchall()

    buildings_list = []

    for row in data2:
        buildings_list.append(row[1].encode('ascii', 'ignore'))

    return buildings_list

#SQLITE execute
def sqlite_update(session, server):
    
    html = session.get('http://{0}/dorf1.php'.format(server))
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
    DROP TABLE IF EXISTS map_info;

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
    );

    CREATE TABLE map_info ( 
        village_id INTEGER NOT NULL,
        type TEXT NOT NULL,
        x INTEGER NOT NULL, 
        y INTEGER NOT NULL,
        distance TEXT NOT NULL,
        inhabitants TEXT,
        player TEXT,
        village TEXT,
        alliance TEXT,
        nation TEXT,
        field_type TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS build_queue (
        id         INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        village_id INTEGER NOT NULL,
        gid   INTEGER NOT NULL,
        aid    INTEGER NOT NULL,
        level  INTEGER NOT NULL,
        active INTEGER NOT NULL,
        timer INTEGER NOT NULL,
        cancel_link TEXT NOT NULL
        )
    ''')

    cur.execute('''INSERT INTO resources(lumber, clay, iron, crop, lumber_prod,
    clay_prod, iron_prod, crop_prod) VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
    (update_lumber_stock(my_soup), update_clay_stock(my_soup), update_iron_stock(my_soup), 
        update_crop_stock(my_soup), update_lumber_prod(my_soup),update_clay_prod(my_soup),
        update_iron_prod(my_soup), update_crop_prod(my_soup)))

    cur.execute('''INSERT INTO storage(warehouse, granary) VALUES(?, ?)''',
        (update_warehouse(my_soup), update_granary(my_soup)))

    values_to_insert = get_spot_info(session, server)

    cur.executemany('''
        INSERT INTO spots ('village_id','id', 'gid', 'level')
        VALUES (?, ?, ?, ?)''', values_to_insert) 

    values_to_insert = create_buildings_list()

    cur.executemany('''
        INSERT INTO buildings ('gid', 'name', 'req1', 'req2', 'req3')
        VALUES (?, ?, ?, ?, ?)''', values_to_insert)
    
    conn.commit()

def upgrade_link(session, server, building_id):

    html = session.get("http://{0}/build.php?id={1}".format(server, building_id))
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

def is_building(village_id, session, server):
    # This function inserts build_info into sqlite, or returns False
    try:
        #SQLITE code
        conn = sqlite3.connect('travdate.sqlite')
        cur = conn.cursor()
        #request and soup
        req = session.get('http://{0}/dorf2.php'.format(server))
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
        #cancel_link
        cancel_btn = re.findall(r".*<a\shref.*", str(soup))
        cancel_btn = cancel_btn[17]
        cancel_btn = cancel_btn.replace(" ", "")
        cancel_btn = cancel_btn.replace("<ahref=\"", "")
        cancel_btn = cancel_btn.replace("\">", "")
        cancel_btn = cancel_btn.replace("amp;", "")
        print cancel_btn
        #SQL execute
        cur.execute('''INSERT INTO build_queue(village_id, gid, aid, level, active, timer, cancel_link)
        VALUES(?, ?, ?, ?, ?, ?, ?)''',
        (village_id, gid_info, aid_info, level_info, "1", time_left, cancel_btn))
        conn.commit()
        return True
    except TypeError:    
        return False

#2 scpravnute subory, soup a js
#Transform coordinates into distance between them
def transform_coordinates(a,b):
    if a < 0:
        if b < 0:
            base = abs(a) - abs(b)
        elif b > 0:
            base = abs(a) + abs(b)
        else:
            base = abs(a)
    elif a > 0:
        if b < 0:
            base = abs(a) + abs(b)
        elif b > 0:
            base = abs(a) - abs(b)
        else:
            base = abs(a)
    else:
        base = abs(b)
    return abs(base)
 
#Calculate distance between 2 tiles on the map
def get_tile_distance(x1,y1,x2,y2):
    """
    Berie ako argumenty coordinaty dvoch policok,
    a vypocita vyslednu vzdialenost.
    """
 
    if x1 == x2:
        return transform_coordinates(y1,y2)
    elif y1 == y2:
        return transform_coordinates(x1,x2)
    elif x1 == x2 and y1 == y2:
        return 0
    else:
        basex = transform_coordinates(x1,x2)
        basey = transform_coordinates(y1,y2)
        base = basex*basex + basey*basey
        base = math.sqrt(base)
        decimal.getcontext().prec = 7
        base = decimal.Decimal(base).quantize(
            decimal.Decimal('0.0'),
            rounding=decimal.ROUND_HALF_UP)
        return base


def get_ajax_token(session, server):
    """
    Bere ako argument session,
    spravy request, a returnuje ajax_id.
    """
 
    r1 = session.get('http://{0}/dorf2.php'.format(server))
    unicodeData = r1.text
    unicodeData.encode('ascii', 'ignore')
    soup = BeautifulSoup(unicodeData, 'html.parser')
    ajax_id = re.findall(r"window\.ajaxToken\s=.*", str(soup))
    ajax_id = str(ajax_id).split("'")
    ajax_id = ajax_id[1]
    return ajax_id
 
def get_tile(x,y,session,server):

    """
    Bere ako argumenty coordinaty policka,
    Spravy kompletny request a login, 
    returnuje cele html ako string.
    """ 
    payload = {'cmd': "viewTileDetails",'x': x, 'y': y,  'ajaxToken': get_ajax_token(session, server)}
    req = session.post('http://{0}/ajax.php?cmd=viewTileDetails'.format(server), data=payload)
    file = open("javascript.txt", "w+")
    file.write(req.content)
    file.close
    return req.content 
 

def make_file(data, file_name):

    file_name = open(file_name, "w+")
    file_name.write(data)
    file_name.close()

def make_soup(x,y,session,server):

    """
    Tato funkcia vola funkcia get_tile(), ktora robi request
    Spravy nam textovy subor ajaxsoup.txt, scrapnute html.
    + returnuje soup, lebo sa pouziva v inych funkciach.
    """
    tile_info = get_tile(x,y,session,server)
    soup = BeautifulSoup(tile_info, 'html.parser')
    soup_file = soup.encode('ascii', 'ignore')
    make_file(soup_file, "ajaxsoup.txt")
    return soup
    
#villages
#3, 3, 3, 9 = village-1
#3, 4, 5, 6 = village-2 , 
#4, 4, 4, 6 = village-3
#4, 5, 3, 6 = village-4
#5, 3, 4, 6 = village-5
#1, 1, 1, 15 =village-6
#4, 4, 3, 7 = village-7
#3, 4, 4, 7 = village-8
#4, 3, 4, 7 = village-9
#3, 5, 4, 6 = village-10
#4, 3, 5, 6 = village-11
#5, 4, 3, 6 = village-12

#oasis
#50% clay            = oasis-8-
#50% iron            = oasis-12-
#25% lumber,crop     = oasis-3-
#50% crop            = oasis-15-
#25% crop            = oasis-14-
#50% lumber          = oasis-4-
#25% iron, crop      = oasis-11-

#25% lumber          = oasis-2-
#25% clay            = oasis-6-
#25% iron            = oasis-10-
#25% clay, crop      = oasis-7-


def get_tile_type():  # tato funkcia returnuje tuple ("village", 9) , alebo (oasis, 2), !!POZOR!! 
    
    #Ak je to village, treba zistit ci je to hrac, h1 tag je meno dediny.  , + obyvatelia, vzdialenost, aliancia.

    tile_type_list = ["village", "oasis", "landscape"] 

    file = open("javascript.txt", "r+")
    soup = BeautifulSoup(file, "html.parser")
    vlg_re = r"<div\sclass='\\\"village'\sid='\\\"tileDetails\\\"'\svillage-.."
    village_re = re.findall(vlg_re, str(soup))
    oas_re = r"<div\sclass='\\\"oasis'\sid='\\\"tileDetails\\\"'\soasis-.."
    oasis_re = re.findall(oas_re, str(soup))
    land_re = r"<div\sclass='\\\"landscape'\sid='\\\"tileDetails\\\"'\slandscape"
    landscape_re = re.findall(land_re, str(soup))
    re_list = [village_re, oasis_re, landscape_re]

    for regex in re_list:
        if regex:
            the_re = regex

    try:
        final_re = re.findall(r"\d+", str(the_re))
        tile_id = final_re[0]

        for x in tile_type_list:
            if x in the_re[0]:

                return (x, tile_id)
    except IndexError:
        return ("landscape", "0")


# tato funkcia vezme ako argument get_tile_type(), returnuje , typ policka + basic staty
def get_tile_info(tile_info):

    villages = {"1": [3,3,3,9], "2": [3,4,5,6], "3": [4,4,4,6], "4": [4,5,3,6], "5": [5,3,4,6],
    "6": [1,1,1,15], "7": [4,4,3,7], "8": [3,4,4,7], "9": [4,3,4,7], "10": [3,5,4,6],
    "11": [4,3,5,6], "12": [5,4,3,6]}

    oasis = {"2": "lumber 25%", "6": "clay 25%", "10": "iron 25%", "14": "crop 25%", 
    "8": "clay 50%", "12": "iron 50%", "4": "lumber 50%", "15": "crop 50%",
    "3": "lumber+crop 25%", "11": "iron+crop 25%", "7": "clay+crop 25%"}

    if tile_info[0] == "village":
        file = open("javascript.txt", "r+")
        soup = BeautifulSoup(file, "html.parser")
        return tile_info[0], villages[tile_info[1]]
    
    if tile_info[0] == "oasis":
        return tile_info[0], oasis[tile_info[1]], find_monsters()

    if tile_info[0] == "landscape":
        return "landscape"
    else:
        print "no match"



def find_monsters():  #neukazuje to ake su to monstra, ked to bude treba tak dorobit.
    """
    returns monsters @oasis, as a list.[7, 5, 5], this funkcion is used in get_tile_info()
    in current state, it takes data from text document that has already been scraped
    """
    try:
        file = open("javascript.txt", "r+")
        #file = open("oasismonsters.txt", "r+")
        data = file.read()
        file.close()

        oasis_monsters = re.findall(r"<img class=\\\"unit.{1250}", str(data))
        oasis_monsters = oasis_monsters[0].split(" ")
        oasis_monsters = filter(None, oasis_monsters)
        monster_list = []
        for string in oasis_monsters:
            if len(string) <3: 
                monster_list.append(string)

        return monster_list
    except IndexError:
        return "Empty"


def is_player(x,y,session,server): # Tato funkcia zisti ci je na policku dedina alebo je prazdne, ak je prazdne vrati False, ale je tam dedina True.

    # Sprav tu if aby to zistilo ci tam je dedina, ak ano return True
    data = make_soup(x,y,session,server)
    try:
        village_name = re.findall(r"<h1>.{20}", str(data))
        vllg_name = village_name[0].split("\\")
        vllg_name = vllg_name[0].split("<h1>")
        vllg_name = vllg_name[1]

        if vllg_name:
            return True
        else:
            return False
    except IndexError:
        return False

def get_complex_info(my_x, my_y, x, y,session,server):
    #tato funkcia vezme ako argumenty: is_player funkciu, aj je is_player True, 
    #returne to info o hracovej dedine, ak je False returne to info o policku
    distance = get_tile_distance(my_x, my_y, x, y) # distance chceme tak ci tak
    player = is_player(x,y,session,server)

    file = open("javascript.txt", "r")
    data = file.read()
    file.close()
    
    dict_values = {"type": "",
                    "x": str(0),
                    "y": str(0),
                    "distance": distance,
                    "inhabitants": "",
                    "player": "",
                    "village_name": "",
                    "alliance": "",
                    "nation": "",
                    "field_type": ""
                    }   

    if player == True: #ak je tam dedina nejakeho hraca
        #village_name
        try:
            village_name = re.findall(r"<h1>.{20}", data)
            vllg_name = village_name[0].split("\\")
            vllg_name = vllg_name[0].split("<h1>")
            vllg_name = vllg_name[1]
            #player name
            player_name = re.findall(r"<a\shref=\\\"spieler\.php\?uid=....\\\">.{10}", data)
            player_name = player_name[0].split("\\\">")
            player_name = player_name[1].split("<")
            player_name = player_name[0]
            #population
            population = re.findall(r"<a\shref=\\\"spieler\.php\?uid=....\\\">.{100}", data)[0]
            population = population.split("<td>")
            population = population[1].split("<")
            population = population[0]
            #alliance
            alliance = re.findall(r"<a\shref=\\\"allianz.php\?aid=.{10}", data)
            alliance = alliance[0].split(">")
            alliance = alliance[1].split("<")
            alliance = alliance[0]
            #nation
            nation = re.findall(r"class=\\\"first\\\">.{60}", data)
            nation = nation[0].split("<td>")
            nation = nation[1].split("<")
            nation = nation[0]

            
            #if it's a village controlled by a player
            dict_values = {"type": get_tile_type()[0],
                           "x": x,
                           "y": y,
                           "distance": distance,
                           "inhabitants": population,
                           "player": player_name,
                           "village_name": vllg_name,
                           "alliance": alliance,
                           "nation": nation,
                           "field_type": get_tile_info(get_tile_type())[1]
                        }
        # if its an Oasis
        except IndexError:
            dict_values["type"] = get_tile_type()[0]
            dict_values["x"] = x
            dict_values["y"] = y
            dict_values["inhabitants"] = find_monsters()
            dict_values["player"] = ""
            dict_values["alliance"] = ""
            dict_values["nation"] = ""
            dict_values["field_type"] = get_tile_info(get_tile_type())[1]
        return dict_values

    if player == False:
        #if its an empty village
        dict_values["type"] = get_tile_type()[0]
        dict_values["x"] = x
        dict_values["y"] = y
        dict_values["inhabitants"] = str(0)
        dict_values["player"] = ""
        dict_values["alliance"] = ""
        dict_values["nation"] = ""
        dict_values["field_type"] = get_tile_info(get_tile_type())[1]

        return dict_values
    else:
        return False


def map_scan(centerx, centery, scope, session, server):
    i = centerx - scope
    endi = i+(scope*2)+1
    conn = sqlite3.connect('travdate.sqlite')
    cur = conn.cursor()

    while(i < endi):
        j = centery + scope
        endj = j-(scope*2)-1
        while(j > endj):
            if i == centerx and j == centery:
                print "haha"
            else:
                map_info_values = get_complex_info(centerx, centery, i, j, session, server)
                print map_info_values
                if map_info_values == False:
                    print "skip"
                else:
                    cur.execute('''INSERT INTO map_info(village_id, type, x, y, distance, inhabitants,
                        player, village, alliance, nation, field_type) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                        (1, map_info_values["type"], map_info_values["x"],map_info_values["y"],
                        str(map_info_values["distance"]), str(map_info_values["inhabitants"]),
                        map_info_values["player"], map_info_values["village_name"],
                        map_info_values["alliance"], map_info_values["nation"],
                        str(map_info_values["field_type"])))
                    conn.commit()
            j = j - 1
        i = i + 1
