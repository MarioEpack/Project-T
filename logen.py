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
#Ak uz subor existuje tak ho nebudem vytvarat znova
if my_file.is_file() == False:
    file = open("testfile.txt","w")
    file.write(str(my_soup))
    file.close()


######
###### Scraping the basic info
mish_mash = my_soup.find_all('span')
#drevo = l1, hlina = l2, zelezo = l3, obilie = l4 , treba to vybrat z mish_mash
mish_mash = list(mish_mash)
#Zhruba vybrate zatial
warehouse = mish_mash[4]
granary = mish_mash[8]
lumber = mish_mash[5]
clay = mish_mash[6]
iron = mish_mash[7]
crop = mish_mash[9]
storage = [lumber, clay, iron, crop]
ware_and_granary = [warehouse, granary]

def update_stock():
    for stock in storage:
        value_re = re.findall(r'\d', str(stock))
        value_re.remove(value_re[0])
        value = ''.join(value_re)
        print value
        

def update_gra_and_ware():
    for stock in ware_and_granary:
        value_re = re.findall(r'\d', str(stock))
        value = ''.join(value_re)
        print value
        

def total_update():
    update_stock()
    update_gra_and_ware()

total_update()
