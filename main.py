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
        self.bck = BackEnd()
        tm = self.theme_cls
        tm.theme_style = 'Dark'
        tm.primary_palette = 'Green'
        self.sm = MDScreenManager()
        self.sm.add_widget(Main())
        self.sm.add_widget(Create())
        return self.sm

    def on_start(self): ...
        

    def cadastrarUsuario(self, email, pwd, nome): ...

    def login(self, email, pwd): ...
        
    def verificar(self): ...

PDV().run()