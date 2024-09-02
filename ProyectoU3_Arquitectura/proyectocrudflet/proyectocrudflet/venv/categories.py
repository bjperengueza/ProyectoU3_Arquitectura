import flet as ft
import requests

API_URL = "http://127.0.0.1:4200/api/categories/"

def home_page_categories(page: ft.Page):
    def show_snackbar(message):
        snack_bar = ft.SnackBar(ft.Text(message))
        page.overlay.append(snack_bar)
        snack_bar.open = True
        page.update()

    def load_categories(search_query=""):
        items = []
        try:
            response = requests.get(API_URL)
            response.raise_for_status()
            categories = response.json()
        except requests.exceptions.RequestException as e:
            show_snackbar(f"Error al obtener categorías: {e}")
            return

        for category in categories:
            if search_query.lower() in category['name'].lower():
                item = ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Text(category['name'], weight="bold"),
                            ft.Row(
                                controls=[
                                    ft.IconButton(
                                        icon=ft.icons.EDIT,
                                        on_click=lambda e, c=category: edit_category_handler(e, c)
                                    ),
                                    ft.IconButton(
                                        icon=ft.icons.DELETE,
                                        on_click=lambda e, c_id=category['id']: delete_categories_handler(e, c_id)
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.END
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    padding=ft.padding.all(10)
                )
                items.append(item)

        list_view.controls = items
        page.update()

    def validate_inputs():
        errors = False
        if not name_field.value.isalpha():
            name_error.value = "El nombre debe contener solo letras."
            errors = True
        else:
            name_error.value = ""

        page.update()
        return not errors

    def add_category_handler(e):
        if not validate_inputs():
            return

        try:
            response = requests.post(API_URL, json={"name": name_field.value})
            response.raise_for_status()
            load_categories(search_field.value)
            name_field.value = ""
        except requests.exceptions.RequestException as e:
            show_snackbar(f"Error al agregar categoría: {e}")

        page.update()

    def edit_category_handler(e, category):
        name_field.value = category['name']
        page.update()

        def save_edits(e):
            try:
                response = requests.put(f"{API_URL}{category['id']}", json={"name": name_field.value})
                response.raise_for_status()
                load_categories(search_field.value)
                name_field.value = ""
                page.dialog.open = False
                page.update()
            except requests.exceptions.RequestException as e:
                show_snackbar(f"Error al actualizar categoría: {e}")

        page.dialog = ft.AlertDialog(
            title=ft.Text("Editar Categoría"),
            content=ft.Column([
                name_field,
                name_error
            ]),
            actions=[
                ft.TextButton("Guardar", on_click=save_edits),
                ft.TextButton("Cancelar", on_click=lambda _: close_dialog())
            ]
        )
        page.dialog.open = True
        page.update()

    def close_dialog():
        page.dialog.open = False
        page.update()

    def delete_categories_handler(e, category_id):
        try:
            response = requests.delete(f"{API_URL}{category_id}")
            response.raise_for_status()
            load_categories(search_field.value)
        except requests.exceptions.RequestException as e:
            show_snackbar(f"Error al eliminar categoría: {e}")

        page.update()

    def search_handler(e):
        load_categories(search_field.value)

    def logout_handler(e):
        page.show_login_page()

    # Campo de entrada para el nombre con icono y validación
    name_field = ft.TextField(
        label="Nombre",
        prefix_icon=ft.icons.LABEL,
        on_change=lambda e: validate_inputs()
    )
    name_error = ft.Text("", color=ft.colors.RED)

    # Campo de búsqueda con icono
    search_field = ft.TextField(
        label="Buscar Categorías",
        prefix_icon=ft.icons.SEARCH,
        on_change=search_handler
    )

    # Botones con iconos
    search_button = ft.ElevatedButton(
        text="Buscar",
        on_click=search_handler,
        icon=ft.icons.SEARCH
    )
    add_button = ft.ElevatedButton(
        text="Agregar Categoría",
        on_click=add_category_handler,
        icon=ft.icons.ADD
    )
    logout_button = ft.ElevatedButton(
        text="Cerrar Sesión",
        on_click=logout_handler,
        icon=ft.icons.LOGOUT
    )

    # Lista de categorías
    list_view = ft.ListView(
        auto_scroll=True,
        width=600,
        height=200
    )

    # Añadir los controles a la página
    page.add(
        search_field,
        search_button,
        name_field,
        name_error,
        add_button,
        list_view,
        logout_button
    )

    # Cargar categorías
    load_categories()

# if __name__ == "__main__":
#     ft.app(target=home_page_categories)
