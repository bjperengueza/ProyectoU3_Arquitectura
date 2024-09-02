import flet as ft
from login import login_page
from navegacion import navegation

def main(page: ft.Page):
    page.title = "Sistema CRUD de Productos"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    def show_login_page():
        page.clean()
        login_page(page)

    def show_home_page():
        page.clean()
        navegation(page)

    # Asignar funciones de navegación
    page.show_login_page = show_login_page
    page.show_home_page = show_home_page

    # Inicializa la página de inicio de sesión
    show_login_page()

ft.app(target=main)
