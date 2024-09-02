import flet as ft
import requests
from werkzeug.security import check_password_hash
from navegacion import navegation
def authenticate_user(username, password):
    try:
        response = requests.get('http://localhost:4300/api/users')
        if response.status_code == 200:
            users = response.json()
            user = next((u for u in users if u['username'] == username), None)
            if user and check_password_hash(user['password'], password):
                return user
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con la API: {e}")
    return None

def login_page(page: ft.Page):
    def login_handler(e):
        username = username_field.value
        password = password_field.value
        user = authenticate_user(username, password)
        
        if user:
            show_home_page(page)  # Llama a la función para redirigir a la navegación principal
        else:
            error_message.value = "Nombre de usuario o contraseña incorrectos."
            error_message.visible = True
            page.update()

    def show_home_page(page):
        # Limpia la página actual y luego redirige a la función de navegación principal
        page.clean()
        navegation(page)  # Asume que 'navegation' es la función que maneja la navegación principal

    username_field = ft.TextField(
        label="Nombre de Usuario",
        prefix_icon=ft.icons.SUPERVISED_USER_CIRCLE,
        max_length=15,
        helper_text="Máximo 15 caracteres"
    )
    
    password_field = ft.TextField(
        label="Contraseña",
        password=True,
        prefix_icon=ft.icons.PASSWORD_OUTLINED,
        max_length=10,
        helper_text="Máximo 10 caracteres"
    )
    
    login_button = ft.ElevatedButton(
        icon=ft.icons.LOGIN_OUTLINED,
        icon_color="blue500",
        text="INICIAR SESIÓN",
        on_click=login_handler
    )
    
    login_image = ft.Image(
        src="C:/Users/jhon.zambrano/Documents/respaldos/proyectocrudflet/venv/icon.jpg",
        fit=ft.ImageFit.CONTAIN,
        border_radius=12,
        width=300,
        height=150
    )
    
    error_message = ft.Text(
        value="",
        color=ft.colors.RED,
        visible=False
    )
    
    centered_container = ft.Container(
        content=ft.Column(
            [
                login_image,
                username_field,
                password_field,
                login_button,
                error_message
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        alignment=ft.alignment.center,
        padding=100
    )
    
    page.add(centered_container)

if __name__ == "__main__":
    ft.app(target=login_page)
