from flet import *

def main(page: Page):
    class Cardx(Card):
        def __init__(self, Icone=icons.MONITOR_HEART_OUTLINED, Titulo = 'Titulo', Sub = 'Subtitulo'):
            super().__init__()
            self.content = Container(
                content=Column([
                            ListTile(
                            leading=Icon(Icone),
                            title=Text(Titulo),
                            subtitle=Text(Sub),
                            )
                    ], alignment=MainAxisAlignment.CENTER),
                    width=400,
                    padding=5
                )
    def HOME(x):
        a = x.control.selected_index
        if a == 1:
            home.visible = True
            page.update()
        else:
            home.visible = False
            page.update()
            
    nomeApp = 'Peguete.io'
    nomeUser = 'Guilherme'
    page.window_width = 400
    page.title = nomeApp
    page.padding = 50
    page.vertical_alignment = MainAxisAlignment.CENTER
    
    page.appbar = AppBar(
        title=Text(nomeApp),
        center_title=False,
        leading=Icon(icons.HEART_BROKEN_ROUNDED)
    )
    page.navigation_bar = NavigationBar(
        destinations=[
            NavigationDestination(icon=icons.WINDOW, label='Dashboard'),
            NavigationDestination(icon=icons.HOME, label='Home'),
            NavigationDestination(icon=icons.PERSON, label='Perfil'),
        ],
        on_change=HOME
    )
    
    home = Container(
                Column([
                        Text(f'Seja bem vindo, {nomeUser}, Qual seu relato pra hoje?'),
                        Cardx(Icone=icons.MONITOR_HEART_OUTLINED, Titulo='Ultimo Relato !',Sub='05/11/2022 - Conheci uma garota cahamda Ingrid, na real eu ja a conheci, mas agora parece ser diferente...'),
                        Cardx(Icone=icons.DONE_ALL, Titulo = 'Estado Emocional:', Sub = 'Atualmente apaixonado e construindo uma relação.'),
                        Card(
                            content=Container(
                                content=(
                                    Row([
                                        TextButton(
                                            icon = 'add',
                                            text='Adicionar'
                                        ),
                                        TextButton(
                                            icon = 'REFRESH',
                                            text='Atualizar'
                                        ),
                                    ], alignment=MainAxisAlignment.CENTER)
                                )
                            )
                            ),
                    ]),
                visible=False,
                )
    
    page.add(home)
app(target=main)