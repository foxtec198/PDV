from datetime import datetime as dt
import requests as rq

class PDV:
    def __init__(self):
        self.link = 'https://pdv-v1-aeffb-default-rtdb.firebaseio.com/'
        # self.cadastrarProdutos(789456125, 'Redmi 12C', 'Celulares', 899, 1299, 5)
        self.excluirProdutos('789456123')

    def consultaCategorias(self):
        r = rq.get(f'{self.link}Categorias/.json')
        self.d = r.json()
            
    def cadastrarCategorias(self, ctg):
        valores = {'Nome': ctg}
        self.consultaCategorias()
        
        for id in self.d:
            self.dados = self.d[id]
            if ctg.lower() == self.dados['Nome'].lower():
                print(f'Categoria {ctg} Ja existe')
                exist = True
                break
            else: exist = False
        if not exist:
            print(f'Categoria {ctg} adicionada com sucesso')
            rq.post(f'{self.link}Categorias/.json', json=valores)
    
    def excluirCategorias(self, ctg):
        self.consultaCategorias()
        for id in self.d:
            dados = self.d[id]
            if ctg.lower() == dados['Nome'].lower():
                r = rq.delete(f'{self.link}/Categorias/{id}.json')  
                print(f'Categoria {ctg} excluida com sucesso')
                break
            
    def cadastrarProdutos(self, ean, nome, categoria, valorCusto, valorVenda, quantidade):
        self.consultarProdutos()
        for id in self.todosProdutos:
            prod = self.todosProdutos[id]
            if prod['EAN'] == int(ean):
                exist = True
                break
            else: exist = False
        if not exist:
            self.dc = {
                'EAN': ean,
                'Nome': nome,
                'Categoria': categoria,
                'Valor de Custo': valorCusto,
                'Valor de Venda': valorVenda,
                'Quantidade': quantidade
                }
            rq.post(f'{self.link}/Produtos.json', json = self.dc)
        
    def consultarProdutos(self):
        r = rq.get(f'{self.link}/Produtos.json')
        self.todosProdutos = r.json()

    def excluirProdutos(self, ean):
        self.consultarProdutos()
        for id in self.todosProdutos:
            prod = self.todosProdutos[id]
            if int(ean) == int(prod['EAN']):
                nome = prod['Nome']
                r = rq.delete(f'{self.link}/Produtos/{id}.json')  
                print(f'Produto {nome} excluido com sucesso')
                break
            
    def adicionarProdutos(self):
        ...
            

        

if __name__ == "__main__":
    PDV()