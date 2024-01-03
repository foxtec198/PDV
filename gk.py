from random import randint
import requests as rq

link = 'https://pdv-v1-aeffb-default-rtdb.firebaseio.com/adm/keys.json'

class Gk:
    def addValue(self):
        self.key = randint(100000, 999999)
        self.consValue()
        if not self.exist:
            dd = {'key' : self.key, 'verify' : False}
            rq.post(link, json=dd)
            print(f'Chave {self.key} adicionada!')
        
    def consValue(self):
        r = rq.get(link)
        ids = r.json()
        self.exist = False
        if ids != None:
            for id in ids:
                if self.key == ids[id]['key']:
                    self.exist = True
                    break

g = Gk()
for i in range(1, 21):
    g.addValue()