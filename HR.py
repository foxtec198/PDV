from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivymd.tools.hotreload.app import MDApp

class FirstLogin(MDScreen):
    ...
    
class Main(MDScreen):
    ...
    
class Login(MDScreen):
    ...
    
class Create(MDScreen):
    ...

class PDV(MDApp):
    KV_FILES = ['src/style.kv']
    DEBUG = True
    def build_app(self):
        th = self.theme_cls
        th.theme_style = 'Dark'
        th.primary_palette = 'Green'
        Builder.load_file('src/style.kv')
        sm = MDScreenManager()
        sm.add_widget(Main())
        sm.add_widget(FirstLogin())
        sm.add_widget(Login())
        sm.add_widget(Create())
        self.root.current = 'create'
        return sm
PDV().run()