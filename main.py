from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.toast import toast
from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from app import *

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
        self.auth = Auth()
        self.adm = Admin()
        Builder.load_file('./src/style.kv')
        tm = self.theme_cls
        tm.theme_style = 'Dark'
        tm.primary_palette = 'Green'
        self.sm = MDScreenManager()
        self.sm.add_widget(Login())
        self.sm.add_widget(Create())
        self.sm.add_widget(Main())
        return self.sm

    def on_start(self):
        self.idsMain = self.root.get_screen('main').ids
        self.idsMain.mainLogo.source = self.adm.get_logo()
        self.idsMain.lblLoja.text = self.adm.get_name()

        if not self.adm.loja_existent():
            self.sm.add_widget(FirstLogin())
            self.root.current = 'FL'
        else: self.root.current = 'login'
        if self.adm.verify_login(): 
            self.root.current = 'main'
        
    def cadastrarUsuario(self, email, pwd, nome):
        res = self.auth.create(email, pwd, nome)
        if res == 'Sucesso':
            toast(res)
            self.root.current = 'main'
        else: toast(res)

    def login(self, email, pwd):
        res = self.auth.login(email, pwd)
        if res == 'Sucesso': 
            toast(res)
            self.root.current = 'main'
        else: toast(res)
        
    def verificar(self, user, pwd):
        res = Admin().login(user, pwd)
        if res == 'Sucesso': self.root.current = 'login'
        else: toast(res)
    
    def logout(self):
        self.adm.update_verify(False)

PDV().run()