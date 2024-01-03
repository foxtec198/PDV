from random import randint
import requests as rq

link = 'https://pdv-v1-aeffb-default-rtdb.firebaseio.com/Lojas/adm/keys.json'

def addValue():
    global key
    key = randint(100000, 999999)
    consValue()
    if not exist:
        dd = {'key' : key, 'verify' : False}
        rq.post(link, json=dd)
    
def consValue():
    global exist
    r = rq.get(link)
    ids = r.json()
    if ids != None:
        for id in ids:
            if key == ids[id]['key']:
                exist = True
                break
            else: exist = False
    else: exist = False

for i in range(1, 21):
    addValue()