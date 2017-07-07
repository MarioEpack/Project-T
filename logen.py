import requests
import re
from pathlib import Path
from bs4 import BeautifulSoup


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
           'name': 'Ashreen', 
           'password': 'testing', 
           's1': 'Login', 
           'w': '1920:1080'}
session = requests.Session()


r2 = session.post('http://ts2.travian.sk/dorf1.php', data=payload, cookies=r1.cookies)
r3 = session.get('http://ts2.travian.sk/dorf1.php', cookies=r2.cookies)
unicodeData = r3.text
my_soup = BeautifulSoup(unicodeData, 'html.parser')

my_file = Path("/home/epack/Pythonstuff/TravianProject/testfile.txt")
#Ak uz subor existuje tak ho nebudem vytvarat znova, zmen si tento path na svoj
if my_file.is_file() == False:
    file = open("testfile.txt","w")
    file.write(str(my_soup))
    file.close()


######
###### Scraping the basic info
#STORAGE
#drevo = l1, hlina = l2, zelezo = l3, obilie = l4 , treba to vybrat zo soup_storage

#UPDATE STORAGE FUNCTIONS

def update_lumber_stock():
    lumber_storage = my_soup.find(id= "l1")
    value_re = re.findall(r'\d', str(lumber_storage))
    value_re.remove(value_re[0])
    value = ''.join(value_re)
    return value + ' lumber stock.'

def update_clay_stock():
    clay_storage = my_soup.find(id= "l2")
    value_re = re.findall(r'\d', str(clay_storage))
    value_re.remove(value_re[0])
    value = ''.join(value_re)
    return value + ' clay stock.'

def update_iron_stock():
    iron_storage = my_soup.find(id= "l3")
    value_re = re.findall(r'\d', str(iron_storage))
    value_re.remove(value_re[0])
    value = ''.join(value_re)
    return value + ' iron stock.'

def update_crop_stock():
    crop_storage = my_soup.find(id= "l4")
    value_re = re.findall(r'\d', str(crop_storage))
    value_re.remove(value_re[0])
    value = ''.join(value_re)
    return value + ' crop stock.'

def update_warehouse():
    warehouse_storage = my_soup.find(id="stockBarWarehouse")
    value_re = re.findall(r'\d', str(warehouse_storage))
    value = ''.join(value_re)
    return value + ' current warehouse stock.'

def update_granary():
    granary_storage = my_soup.find(id="stockBarGranary")
    value_re = re.findall(r'\d', str(granary_storage))
    value = ''.join(value_re)
    return value + ' current granary stock.'

#UPDATE PRODUCTION FUNCTIONS       

def update_lumber_prod():
    soup_lumber_prod = my_soup.find(href="production.php?t=1")
    lumber_prod = re.findall(r'\d', str(soup_lumber_prod))
    lumber_prod.remove(lumber_prod[0])
    lumber = ''.join(lumber_prod)
    return lumber + ' lumber production'

def update_clay_prod():
    soup_clay_prod = my_soup.find(href="production.php?t=2")
    clay_prod = re.findall(r'\d', str(soup_clay_prod))
    clay_prod.remove(clay_prod[0])
    clay = ''.join(clay_prod)
    return clay + ' clay production'

def update_iron_prod():
    soup_iron_prod = my_soup.find(href="production.php?t=3")
    iron_prod = re.findall(r'\d', str(soup_iron_prod))
    iron_prod.remove(iron_prod[0])
    iron = ''.join(iron_prod)
    return iron + ' iron production'

def update_crop_prod():
    soup_crop_prod = my_soup.find(href="production.php?t=4")
    crop_prod = re.findall(r'\d', str(soup_crop_prod))
    crop_prod.remove(crop_prod[0])
    crop = ''.join(crop_prod)
    return crop + ' crop production'

        

def total_update():
    print update_lumber_stock()
    print update_crop_stock()
    print update_iron_stock()
    print update_clay_stock()
    print update_warehouse()
    print update_granary()

    print update_lumber_prod()
    print update_clay_prod()
    print update_iron_prod()
    print update_crop_prod()


total_update()
