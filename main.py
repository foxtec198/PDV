from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.toast import toast
from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from app import BackEnd

class FirstLogin(MDScreen):
    ...

class Main(MDScreen):
    ...

class Login(MDScreen):
    ...
    
class Create(MDScreen):
    ...

class PDV(MDApp):
    def build(self):
        Builder.load_file('./src/style.kv')
        tm = self.theme_cls
        tm.theme_style = 'Dark'
        tm.primary_palette = 'Green'
        self.sm = MDScreenManager()
        self.sm.add_widget(Main())
        self.sm.add_widget(Create())
        return self.sm

    def fl(self):
        self.sm.add_widget(FirstLogin())
        self.idsFirstLogin = self.root.get_screen('FL').ids
        self.root.current = 'FL'
        self.idsFirstLogin.tt.text = "First Login - PDV"

    def on_start(self):
        self.bck = BackEnd()
        self.c = self.bck.c
        self.conn = self.bck.conn
        try: self.bck.verificacaoDeLoja(0, 0)
        except: self.fl() 
        if self.bck.loja != 0 and self.bck.key != 0:
            self.sm.add_widget(Login())
            self.idsLogin = self.root.get_screen('login').ids
            self.idsCreate = self.root.get_screen('create').ids
            self.idsLogin.tt.text = f'{self.bck.nomeLoja} - {self.bck.loja}'
            self.idsCreate.tt.text = f'{self.bck.nomeLoja} - {self.bck.loja}'
            self.root.current = 'login'
        else:
            self.fl()
        self.idsMain = self.root.get_screen('main').ids

    def cadastrarUsuario(self, cpf, nome, email, pwd):
        self.nomeUser = nome.split()
        if cpf != '' and nome != '' and email != '' and pwd != '':
            self.c.execute(f'INSERT INTO users(CPF, Nome, Email, Pwd) VALUES ("{cpf}","{nome}","{email}","{pwd}")')
            toast(f'Usuário criado com sucesso, seja bem vindo {self.nomeUser[0]}')
            self.conn.commit()
            self.root.current = 'main'
        else: toast('Credenciais Invalidas')

    def login(self, user, pwd):
        dd = self.c.execute('select CPF, Pwd, Nome from users').fetchall()
        for i in dd:
            cpf = i[0]
            sn = i[1]
            self.nomeUser = i[2].split()
            if user == cpf:
                if pwd == sn:
                    toast(f'Logado, bem vindo {self.nomeUser[0]}')
                    self.root.current = 'main'
                else:
                    toast('Senha incorreta')
            else:
                toast('Usuário não encontrado')
        
    def verificar(self):
        user = self.idsFirstLogin.user.text
        pwd = self.idsFirstLogin.pwd.text
        a = self.bck.verificacaoDeLoja(user, pwd)
        if not a:
            toast('Credenciais Invalidas')
        elif a:
            toast(f'Loja Gerada com Sucesso - {self.bck.loja}')
            self.root.current = 'create'
        else:
            toast('Erro desconhecido!')

if __name__ == '__main__':
    PDV().run()