from time import strftime as st
from sqlite3 import connect
import requests as rq
from random import randint

class BackEnd:
    def __init__(self):
        self.dt = "%d/%m/%Y - %H:%M"
        self.conn = connect('src/myini.db')
        self.c = self.conn.cursor()
        self.link = 'https://pdv-v1-aeffb-default-rtdb.firebaseio.com/Lojas/'
        
    def verificacaoDeLoja(self, uid, pwd):
        self.c.execute('create table if not exists cfg(loja INTEGER, key INT, cidade TEXT, nomeLoja TEXT, logo VARCHAR(100))')
        cfg = self.c.execute('select * from cfg').fetchall()
        if cfg == []:
            self.c.execute('insert into cfg(loja, key, cidade, nomeLoja, logo) Values(0, 0, "Londrina","PDV Server","src/logo.png")')
            self.conn.commit()
            
        cfg = self.c.execute('select * from cfg').fetchall()
        for id in cfg:
            self.loja = id[0]
            self.key = id[1]
            self.cidade = id[2]
            self.nomeLoja = id[3]
            self.logoLoja = id[4]
        
        # PRIMEIRO ACESSO 
        if self.loja == 0 and self.key == 0:
            link = 'https://pdv-v1-aeffb-default-rtdb.firebaseio.com/adm/'
            r = rq.get(f'{link}user/.json')
            d = r.json()
            if uid == d['uid'].lower():
                if pwd == d['pwd']:
                    r = rq.get(f'{link}keys/.json')
                    keys =  r.json()
                    for id in keys:
                        verify = keys[id]['verify']
                        if not verify:
                            key = keys[id]['key']
                            idKey = id
                            nLoja = randint(100000, 999999)
                            rq.patch(f'{link}keys/{idKey}.json', json={'verify':True})
                            print(f'Chave {key} designada com sucesso!')
                            self.c.execute(f'update cfg set loja = "{nLoja}", key = "{key}"')
                            self.conn.commit()
                            cfg = self.c.execute('select * from cfg').fetchall()
                            for id in cfg:
                                self.loja = id[0]
                                self.key = id[1]
                            rq.post(f'{self.link}.json', json={'Loja': {'numero': nLoja, 'Criada': st(self.dt)}})
                            break
                else:
                    print('senha incorreta')
            else:
                print('usuário incorreto')
            
        # VERIFICANDO LOJA 
        r = rq.get(f'{self.link}.json')
        lojas = r.json()
        self.existLoja = False
        if lojas != None:
            for id in lojas:
                dlojas = lojas[id]['Loja']
                if dlojas['numero'] == self.loja:
                    self.id = id
                    self.existLoja = True
                    break
                
        # VERIFICANDO AUT KEY      
        r = rq.get(f'https://pdv-v1-aeffb-default-rtdb.firebaseio.com/adm/keys.json')
        ids = r.json()
        self.existKey = False
        self.verify = False
        if ids != None:
            for id in ids:
                if int(self.key) == ids[id]['key']:
                    self.existKey = True
                    self.verify = ids[id]['verify']
                    break
                
        if self.existLoja and self.existKey and self.verify:
            self.link = f'{self.link}/{self.id}/'
            dd = {'cidade': self.cidade, 'nome da loja': self.nomeLoja}
            rq.patch(f'{self.link}Loja/.json', json=dd)
            return True
        else: return False
            
    def consultaCategorias(self):
        r = rq.get(f'{self.link}Categorias/.json')
        self.d = r.json()
            
    def cadastrarCategorias(self, ctg):
        valores = {'Nome': ctg, 'Data de Cadastro': st(self.dt)}
        self.consultaCategorias()
        
        exist = False
        if self.d != None:
            for id in self.d:
                self.dados = self.d[id]
                if ctg.lower() == self.dados['Nome'].lower():
                    exist = True
                    break
        
        if not exist:
            rq.post(f'{self.link}Categorias/.json', json=valores)
    
    def excluirCategorias(self, ctg):
        self.consultaCategorias()
        if self.d != None:
            for id in self.d:
                dados = self.d[id]
                if ctg.lower() == dados['Nome'].lower():
                    r = rq.delete(f'{self.link}/Categorias/{id}.json')  
                    print(f'Categoria {ctg} excluida com sucesso')
                    break
            
    def cadastrarProdutos(self, ean, nome, categoria, valorCusto, valorVenda, quantidade):
        self.consultarProdutos()
        exist = False
        if self.todosProdutos != None:
            for id in self.todosProdutos:
                prod = self.todosProdutos[id]
                if prod['EAN'] == int(ean):
                    exist = True
                    break
                
        if not exist:
            dc = {
                'EAN': ean,
                'Nome': nome,
                'Categoria': categoria,
                'Valor de Custo': valorCusto,
                'Valor de Venda': valorVenda,
                'Quantidade': quantidade,
                'Data de Entrada': st(self.dt)
                }
            rq.post(f'{self.link}/Produtos.json', json = dc)
        
    def consultarProdutos(self):
        r = rq.get(f'{self.link}/Produtos.json')
        self.todosProdutos = r.json()

    def excluirProdutos(self, ean):
        self.consultarProdutos()
        if self.todosProdutos != None:
            for id in self.todosProdutos:
                prod = self.todosProdutos[id]
                if int(ean) == int(prod['EAN']):
                    nome = prod['Nome']
                    r = rq.delete(f'{self.link}/Produtos/{id}.json')  
                    print(f'Produto {nome} excluido com sucesso')
                    break
            
    def adicionarProdutos(self, ean, quantidade, nome = ''):
        self.consultarProdutos()
        if self.todosProdutos != None:
            for id in self.todosProdutos:
                prod = self.todosProdutos[id]
                if prod['EAN'] == int(ean) or nome.lower() == prod['Nome'].lower():
                    exist = True
                    qAtual = int(prod['Quantidade'])
                    idA = id
                    break
        if exist:
            quantidade += qAtual
            js = {'Quantidade': quantidade}
            rq.patch(f'{self.link}/Produtos/{idA}/.json', json=js)

if __name__ == "__main__":
    BackEnd()