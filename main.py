from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.toast import toast
from kivymd.uix.screen import MDScreen
from kivymd.uix.datatables import MDDataTable
from kivy.lang import Builder
from kivy.metrics import dp
from threading import Timer
from app import *

# TELAS
class FirstLogin(MDScreen):...
class Main(MDScreen):...
class Login(MDScreen):...
class Create(MDScreen):...
class Config(MDScreen):...

# Front End
class PDV(MDApp):
    def build(self):
        Builder.load_file('./src/style.kv')
        self.auth = Auth()
        self.adm = Admin()
        self.loja = Loja()
        self.chart = Charts()
        self.logo = self.adm.get_logo()
        self.nomeLoja = self.adm.get_name()
        tm = self.theme_cls
        tm.theme_style = 'Dark'
        tm.primary_palette = 'Green'
        self.icon = self.logo
        self.title = self.nomeLoja
        self._app_window
        self.sm = MDScreenManager()
        self.sm.add_widget(Login())
        self.sm.add_widget(Create())
        self.sm.add_widget(Main())
        self.sm.add_widget(Config())
        return self.sm

    def on_start(self):
        self.idsMain = self.root.get_screen('main').ids
        self.idsMain.mainLogo.source = self.logo
        self.idsMain.lblLoja.text = self.nomeLoja

        if not self.adm.loja_existent():
            self.sm.add_widget(FirstLogin())
            self.root.current = 'FL'
        else: self.root.current = 'login'
        if self.adm.verify_login():
            self.root.current = 'main'
        self.rows_dt = self.loja.get_produtos()
        self.dt = MDDataTable(
            elevation = 0,
            column_data=[
                ("EAN.", dp(20)),
                ("Nome", dp(30)),
                ("Quantidade", dp(20)),
                ("Ultima Atualização", dp(30)),
                ("Valor", dp(30))
            ],
            row_data=self.rows_dt,
        )
        self.idsMain.cardProd.add_widget(self.dt)
        self.update()
        
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

    def update(self):
        t = Timer(5, self.update)
        t.start()
        self.dt.row_data = self.rows_dt
        self.chart.chart_produtos()
        self.idsMain.produtosChart.source = 'src/produtos.png'
PDV().run()