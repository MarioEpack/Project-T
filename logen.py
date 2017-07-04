import requests 
from BeautifulSoup import *


r1 = requests.get('http://ts2.travian.sk/login.php')
unicodeData = r1.text
unicodeData.encode('ascii', 'ignore')
soup = BeautifulSoup(unicodeData)
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

r3 = session.get('http://ts2.travian.sk/dorf2.php', cookies=r2.cookies)
unicodeData = r3.text
my_soup = BeautifulSoup(unicodeData)
print type(unicodeData)
print type(my_soup)

file = open("testfile.txt","w")
file.write(str(my_soup))
file.close()
