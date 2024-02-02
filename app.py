import requests as rq, json
from random import randint
from sqlite3 import connect
from tkinter import filedialog
from time import strftime as st
import plotly_express as px 
from plotly.io import templates
import pandas as pd
from rembg import remove
from PIL import Image
from functools import cache

conn = connect('src/temp.db')
c = conn.cursor()

def execute(consulta):
    temp = c.execute(consulta)
    conn.commit()
    return temp

def remove_bg(src):
    img = Image.open(src)
    imgRemoved = remove(img)
    imgRemoved.save(src)

execute('CREATE TABLE IF NOT EXISTS Dados(Loja TEXT, Key INTEGER)')
execute('CREATE TABLE IF NOT EXISTS Verify(LG BOOLEAN)')
execute('CREATE TABLE IF NOT EXISTS Config(Logo TEXT, IdLoja TEXT)')

class Auth:
    def __init__(self):
        self.api = 'AIzaSyBcGQ2SCAO7P58Hh2rHqw6II4SoIxesLYw'

    def raised_error(self, requisicao):
        try:
            requisicao['idToken']
            return 'Sucesso'
        except: return requisicao['error']['message']

    def reset_password(self):
        email = self.user['email']
        rq.post(f'https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key={self.api}', data={"requestType":"PASSWORD_RESET","email":email})
        return 'Email enviado com o link para o Reset da Senha !!'

    def login(self, email, pwd):
        link = f'https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key={self.api}'
        if email != '':
            if pwd != '':
                auth = rq.post(link, data = json.dumps({"email": email, "password": pwd, "returnSecureToken": True}))
                res = self.raised_error(auth.json())
                if res == 'Sucesso':
                    self.user = auth.json()
                    Admin().update_verify(True)
                return res
            else: return 'Senha Vazia'
        else: return 'Email vazio'

    def create(self, email, pwd, nome):
        link = f'https://www.googleapis.com/identitytoolkit/v3/relyingparty/signupNewUser?key={self.api}'
        if email != '':
            if nome != '':
                if pwd != '':
                    auth = rq.post(link, data=json.dumps({"email": email, "password": pwd, "returnSecureToken": True}))
                    res = self.raised_error(auth.json())
                    if res == 'Sucesso':
                        temp = self.login(email, pwd)
                        self.update(self.user['idToken'], display_name = nome)
                        return temp
                    else: return res
                else: return 'Senha Vazia'
            else: return 'Nome Vazio'
        else: return 'Email Vazio'

    def update(self, id_token, display_name = None, photo_url = None, delete_attribute = None):
        link = f'https://identitytoolkit.googleapis.com/v1/accounts:update?key={self.api}'
        rq.post(link, data=json.dumps({"idToken": id_token, "displayName": display_name, "photoURL": photo_url, "deleteAttribute": delete_attribute, "returnSecureToken": True}))

class Admin:
    def __init__(self):
        self.link = 'https://gestaopdv-ba13a-default-rtdb.firebaseio.com/admin'
        self.logo_padrao()
    
    @cache
    def loja_existent(self):
        dd = c.execute('select * from Dados').fetchone()
        if dd == None: return False
        else: return True

    def login(self, user, pwd):
        dados = rq.get(f'{self.link}/Users.json').json()
        if not self.loja_existent():
            if dados != None:
                for id in dados:
                    if user == dados[id]['user']:
                        if pwd == str(dados[id]['pwd']):
                            execute(f'INSERT INTO Dados(Loja, Key) VALUES ("PDV Server", "{self.get_key()}")')
                            Loja().criar_loja()
                            return 'Sucesso'
                        else: return 'Senha Incorreta'
                    else: return 'Usuario Invalido'
            else: return 'Banco de Dados Vazio'
        else: return 'Loja já cadastrada'

    def get_key(self):
        uni = rq.get(f'{self.link}/Keys.json').json()
        for id in uni:
            validade = uni[id]['verificada']
            if not validade:
                rq.patch(f'{self.link}/Keys/{id}/.json', data=json.dumps({'verificada':True}))
                return uni[id]['key']

    def unique(self, key):
        uni = rq.get(f'{self.link}/Keys.json').json()
        for id in uni:
            self.uni = uni[id]['key']
            if key != self.uni: return True
            else: return False
            
    def gerar_keys(self, x):
        count = 0
        for i in range(x):
            k = randint(100000, 999999)
            if self.unique(k):
                rq.post(f'{self.link}/Keys.json', data=json.dumps({'key':k, 'verificada':False}))
                count += 1
        print(f'{count} chaaves adicionadas')

    def verify_login(self):
        verify = c.execute('select * from Verify').fetchone()
        if verify == None: execute('INSERT INTO Verify(LG) VALUES(False)')
        if verify != None: verify = verify[0]
        return verify
    
    def update_verify(self, status: bool):
        execute(f'update Verify set LG = {status}')

    def logo_padrao(self):
        dd = c.execute('select * from config').fetchone()
        if dd == None: execute('insert into Config(Logo) VALUES ("src/logo.png")')

    def alterar_logo(self):
        src = filedialog.askopenfilename(title='Selecione sua Logo!', initialdir='Downloads')
        execute(f'update Config set logo = "{src}"')

    @cache
    def get_logo(self):
        logo = c.execute('select * from config').fetchone()
        if logo != None: logo = logo[0]
        elif logo == None: logo = 'src/logo.png' 
        return logo

    @cache
    def get_name(self):
        name = c.execute('select Loja from Dados').fetchone()
        if name != None: name = name[0]
        elif name == None: name = 'PDV Server'
        return name
        
class Loja:
    def __init__(self):
        self.link = 'https://gestaopdv-ba13a-default-rtdb.firebaseio.com/Lojas'
        try: self.id_loja = c.execute('select IdLoja from Config').fetchone()[0]
        except: self.id_loja = ''

    def alterar_nome_loja(self, nome_loja):
        execute(f'update Dados set Loja = "{nome_loja}"')
        rq.patch(f'{self.link}/{self.id_loja}/.json', data=json.dumps({'nome_loja':nome_loja}))

    def criar_loja(self):
        dd = c.execute('select * from Dados').fetchone()
        if dd != None and self.id_loja == None:
            dados = {'nome_loja': dd[0],'numero_loja': dd[1]}
            cr = rq.post(f'{self.link}/.json', data=json.dumps(dados))
            self.id_loja = cr.json()['name']
            execute(f'update Config set IdLoja = "{self.id_loja}"')
        else: return 'Dados vazios!'

    def zerar_id(self):
        execute('update Config set IdLoja = Null')
    
    def cadastro_de_produtos(self, **prod):
        ean = prod['EAN']
        produto = json.dumps({
            "Nome do Produto": prod['nome_produto'],
            "Quantidade": prod['quantidade'],
            "Valor de Compra": prod['valor_de_compra'],
            "Valor de Venda": prod['valor_de_venda'],
            "Ultima Atualização": st('%x'),
            "Horario":st('%X'), })
        rq.patch(f'{self.link}/{self.id_loja}/Produtos/{ean}/.json', data=produto)

    def adicionar_estoque(self, ean, quantidade: int):
        if quantidade > 0:
            self.info_produtos = rq.get(f'{self.link}/{self.id_loja}/Produtos/{ean}/.json').json()
            try:
                quantidade_antiga = self.info_produtos['Quantidade']
                quantidade_antiga += quantidade
                rq.patch(f'{self.link}/{self.id_loja}/Produtos/{ean}/.json', data=json.dumps({'Quantidade': quantidade_antiga}))
                return 'Valor Atualizado'
            except: 
                if self.info_produtos == None: return 'Produto Não Encontrado'
                else: return 'Erro inesperado!'

    def cadastrar_clientes(self): ...
    
    def get_produtos(self):
        self.produtos = rq.get(f'{self.link}/{self.id_loja}/Produtos/.json').json()
        prod = []
        self.produtosSemEan = []
        if self.produtos != None:
            for ean in self.produtos:
                produtos = self.produtos[ean]
                x = (ean, produtos['Nome do Produto'], produtos['Quantidade'], produtos['Ultima Atualização'], produtos['Valor de Venda'])
                prod.append(x)
                self.produtosSemEan.append(produtos)
            return prod
        else: return 'Sem Produtos Disponiveis'

class Charts:
    def __init__(self):
        self.loja = Loja()
        templates.default = 'plotly_dark'
        self.cl = px.colors.sequential.Darkmint_r

    def chart_produtos(self):
        p = self.loja.get_produtos() 
        if p != 'Sem Produtos Disponiveis': 
            df = pd.DataFrame(self.loja.produtosSemEan)
            pie = px.pie(df, values='Quantidade', names='Nome do Produto', color_discrete_sequence=self.cl)
            pie.write_image('src/produtos.png')#width=400, height=400)

        
if __name__ == "__main__":
    c = Charts()
    c.chart_produtos()
    # l = Loja()
    # print(l.get_produtos())