import re
from bs4 import BeautifulSoup
import sqlite3

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
    lumber_prod = re.findall(r'\d', str(soup_lumber_prod))
    lumber_prod.remove(lumber_prod[0])
    lumber = ''.join(lumber_prod)
    return lumber

def update_clay_prod(my_soup):
    soup_clay_prod = my_soup.find(href="production.php?t=2")
    clay_prod = re.findall(r'\d', str(soup_clay_prod))
    clay_prod.remove(clay_prod[0])
    clay = ''.join(clay_prod)
    return clay

def update_iron_prod(my_soup):
    soup_iron_prod = my_soup.find(href="production.php?t=3")
    iron_prod = re.findall(r'\d', str(soup_iron_prod))
    iron_prod.remove(iron_prod[0])
    iron = ''.join(iron_prod)
    return iron

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


#SQLITE execute

def sqlite_update(my_soup):

    #SQLITE code
    conn = sqlite3.connect('travdate.sqlite')
    cur = conn.cursor()

    cur.executescript('''
    DROP TABLE IF EXISTS resources;
    DROP TABLE IF EXISTS storage;

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
        grannary    INTEGER NOT NULL

    )
    ''')

    cur.execute('''INSERT INTO resources(lumber, clay, iron, crop, lumber_prod,
    clay_prod, iron_prod, crop_prod) VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
    (update_lumber_stock(my_soup), update_clay_stock(my_soup), update_iron_stock(my_soup), 
        update_crop_stock(my_soup), update_lumber_prod(my_soup),update_clay_prod(my_soup),
        update_iron_prod(my_soup), update_crop_prod(my_soup)))

    cur.execute('''INSERT INTO storage(warehouse, grannary) VALUES(?, ?)''',
        (update_warehouse(my_soup), update_granary(my_soup)))


    conn.commit()
