from datetime import datetime as dt
import requests as rq

class PDV:
    def __init__(self):
        self.link = 'https://pdv-v1-aeffb-default-rtdb.firebaseio.com/Lojas/'
        self.verificacaoDeLoja()
        
    def verificacaoDeLoja(self):
        with open('my.ini') as file:
            dados = file.readlines()
            self.loja = dados[0].split()[1]
            self.cidade = dados[1].split()[1]
            self.key = dados[2].split()[1]
            self.nomeLoja = dados[3].split()[1]
            self.logoLoja = dados[4].split()[1]
            file.close()
            
        # VERIFICANDO LOJA 
        r = rq.get(f'{self.link}.json')
        lojas = r.json()
        if lojas != None:
            for id in lojas:
                r = rq.get(f'{self.link}{id}/Loja.json')
                dlojas = r.json()
                if dlojas['numero'] == self.loja:
                    self.id = id
                    self.existLoja = True
                    break
            else: self.existLoja = False
        else: self.existLoja = False
                
        # VERIFICANDO AUT KEY      
        r = rq.get(f'{self.link}adm/keys.json')
        ids = r.json()
        if ids != None:
            for id in ids:
                if int(self.key) == ids[id]['key']:
                    self.existKey = True
                    self.verify = ids[id]['verify']
                    break
            else: 
                self.existKey = False
                self.verify = False
        else: 
            self.existKey = False
            self.verify = False
                
        if self.existLoja and self.existKey and self.verify:
            self.link = f'{self.link}/{self.id}/'
            dd = {'cidade': self.cidade, 'Nome da Loja': self.nomeLoja}
            rq.patch(f'{self.link}.json', json=dd)
        else: print(f'Loja = {self.existLoja}, Key = {self.existKey}, Validação = {self.verify}')
            
    def consultaCategorias(self):
        r = rq.get(f'{self.link}Categorias/.json')
        self.d = r.json()
            
    def cadastrarCategorias(self, ctg):
        valores = {'Nome': ctg}
        self.consultaCategorias()
        
        if self.d != None:
            for id in self.d:
                self.dados = self.d[id]
                if ctg.lower() == self.dados['Nome'].lower():
                    print(f'Categoria {ctg} Ja existe')
                    exist = True
                    break
                else: exist = False
        else: exist = False
        
        if not exist:
            print(f'Categoria {ctg} adicionada com sucesso')
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
        if self.todosProdutos != None:
            for id in self.todosProdutos:
                prod = self.todosProdutos[id]
                if prod['EAN'] == int(ean):
                    exist = True
                    break
                else: exist = False
        else: exist = False
        if not exist:
            dc = {
                'EAN': ean,
                'Nome': nome,
                'Categoria': categoria,
                'Valor de Custo': valorCusto,
                'Valor de Venda': valorVenda,
                'Quantidade': quantidade
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
    PDV()