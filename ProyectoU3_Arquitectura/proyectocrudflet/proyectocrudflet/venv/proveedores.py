import flet as ft
import requests

API_URL = "http://127.0.0.1:4400/api/suppliers/"

def home_page_proveedores(page: ft.Page):
    def show_snackbar(message):
        snack_bar = ft.SnackBar(ft.Text(message))
        page.overlay.append(snack_bar)
        snack_bar.open = True
        page.update()

    def load_suppliers(search_query=""):
        items = []
        try:
            response = requests.get(API_URL)
            response.raise_for_status()
            suppliers = response.json()
        except requests.exceptions.RequestException as e:
            show_snackbar(f"Error al obtener proveedores: {e}")
            return

        for supplier in suppliers:
            if search_query.lower() in supplier['name'].lower():
                item = ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Text(supplier['name'], weight="bold"),
                            ft.Row(
                                controls=[
                                    ft.IconButton(
                                        icon=ft.icons.EDIT,
                                        on_click=lambda e, s=supplier: edit_supplier_handler(e, s)
                                    ),
                                    ft.IconButton(
                                        icon=ft.icons.DELETE,
                                        on_click=lambda e, s_id=supplier['id']: delete_suppliers_handler(e, s_id)
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

    def validate_fields():
        valid = True
        if not name_field.value:
            name_error.value = "El campo 'Nombre' es obligatorio."
            valid = False
        elif not name_field.value.isalpha():
            name_error.value = "El campo 'Nombre' solo debe contener texto."
            valid = False
        else:
            name_error.value = ""

        if not contact_name_field.value:
            contact_name_error.value = "El campo 'Nombre Contacto' es obligatorio."
            valid = False
        else:
            contact_name_error.value = ""

        if not contact_email_field.value:
            contact_email_error.value = "El campo 'Email' es obligatorio."
            valid = False
        elif not contact_email_field.value.endswith("@gmail.com"):
            contact_email_error.value = "El campo 'Email' debe ser una dirección de correo Gmail."
            valid = False
        else:
            contact_email_error.value = ""

        if not phone_field.value:
            phone_error.value = "El campo 'Teléfono' es obligatorio."
            valid = False
        elif not phone_field.value.isdigit():
            phone_error.value = "El campo 'Teléfono' solo debe contener números."
            valid = False
        else:
            phone_error.value = ""

        if not address_field.value:
            address_error.value = "El campo 'Dirección' es obligatorio."
            valid = False
        else:
            address_error.value = ""

        page.update()
        return valid

    def add_suppliers_handler(e):
        if not validate_fields():
            return

        supplier_data = {
            "name": name_field.value,
            "contact_name": contact_name_field.value,
            "contact_email": contact_email_field.value,
            "phone": phone_field.value,
            "address": address_field.value
        }

        try:
            response = requests.post(API_URL, json=supplier_data)
            response.raise_for_status()
            load_suppliers(search_field.value)
            name_field.value = ""
            contact_name_field.value = ""
            contact_email_field.value = ""
            phone_field.value = ""
            address_field.value = ""
            dialog_modal.open = False  # Cerrar el diálogo después de agregar
        except requests.exceptions.RequestException as e:
            show_snackbar(f"Error al agregar proveedor: {e}")

        page.update()

    def edit_supplier_handler(e, supplier):
        # Rellenar campos con los datos existentes
        name_field.value = supplier['name']
        contact_name_field.value = supplier['contact_name']
        contact_email_field.value = supplier['contact_email']
        phone_field.value = supplier['phone']
        address_field.value = supplier['address']
        page.update()

        def save_edits(e):
            if not validate_fields():
                return

            updated_supplier_data = {
                "name": name_field.value,
                "contact_name": contact_name_field.value,
                "contact_email": contact_email_field.value,
                "phone": phone_field.value,
                "address": address_field.value
            }

            try:
                response = requests.put(f"{API_URL}{supplier['id']}", json=updated_supplier_data)
                response.raise_for_status()
                load_suppliers(search_field.value)
                name_field.value = ""
                contact_name_field.value = ""
                contact_email_field.value = ""
                phone_field.value = ""
                address_field.value = ""
                page.dialog.open = False
                page.update()
            except requests.exceptions.RequestException as e:
                show_snackbar(f"Error al actualizar proveedor: {e}")

        page.dialog = ft.AlertDialog(
            title=ft.Text("Editar Proveedor"),
            content=ft.Column([
                name_field,
                name_error,
                contact_name_field,
                contact_name_error,
                contact_email_field,
                contact_email_error,
                phone_field,
                phone_error,
                address_field,
                address_error
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

    def delete_suppliers_handler(e, supplier_id):
        try:
            response = requests.delete(f"{API_URL}{supplier_id}")
            response.raise_for_status()
            load_suppliers(search_field.value)
        except requests.exceptions.RequestException as e:
            show_snackbar(f"Error al eliminar proveedor: {e}")

        page.update()

    def search_handler(e):
        load_suppliers(search_field.value)

    def logout_handler(e):
        page.show_login_page()

    def open_supplier_dialog(e):
        dialog_modal.open = True
        page.update()

    # Campos de texto con validaciones
    name_field = ft.TextField(label="Nombre", prefix_icon=ft.icons.PERSON)
    name_error = ft.Text("", color=ft.colors.RED)

    contact_name_field = ft.TextField(label="Nombre Contacto", prefix_icon=ft.icons.PERSON)
    contact_name_error = ft.Text("", color=ft.colors.RED)

    contact_email_field = ft.TextField(label="Email", prefix_icon=ft.icons.EMAIL)
    contact_email_error = ft.Text("", color=ft.colors.RED)

    phone_field = ft.TextField(label="Teléfono", prefix_icon=ft.icons.PHONE)
    phone_error = ft.Text("", color=ft.colors.RED)

    address_field = ft.TextField(label="Dirección", prefix_icon=ft.icons.LOCATION_ON)
    address_error = ft.Text("", color=ft.colors.RED)

    # Dialog para agregar proveedores
    dialog_modal = ft.AlertDialog(
        title=ft.Text("Agregar Proveedor"),
        content=ft.Container(
            content=ft.Column(
                controls=[
                    name_field,
                    name_error,
                    contact_name_field,
                    contact_name_error,
                    contact_email_field,
                    contact_email_error,
                    phone_field,
                    phone_error,
                    address_field,
                    address_error,
                ],
            ),
            width=400,  # Ajusta el ancho del diálogo
            height=600,  # Ajusta la altura del diálogo
            padding=20,  # Agrega algo de espacio alrededor del contenido
        ),
        actions=[
            ft.TextButton("Agregar Proveedor", on_click=add_suppliers_handler),
            ft.TextButton("Cancelar", on_click=lambda e: close_supplier_dialog(e)),
        ],
        open=False
    )

    def close_supplier_dialog(e):
        dialog_modal.open = False
        page.update()

    # Campo de búsqueda con icono
    search_field = ft.TextField(
        label="Buscar Proveedores",
        prefix_icon=ft.icons.SEARCH,
        on_change=search_handler
    )

    search_button = ft.ElevatedButton(
        text="Buscar",
        on_click=search_handler,
        icon=ft.icons.SEARCH
    )

    add_button = ft.ElevatedButton(
        text="Agregar Proveedor",
        on_click=open_supplier_dialog,
        icon=ft.icons.ADD
    )

    logout_button = ft.ElevatedButton(
        text="Cerrar Sesión",
        on_click=logout_handler,
        icon=ft.icons.EXIT_TO_APP
    )

    # Lista de proveedores
    list_view = ft.ListView(
        auto_scroll=True,
        width=600,
        height=200
    )

    # Añadir controles a la página
    page.add(
        search_field,
        search_button,
        add_button,
        list_view,
        logout_button,
        dialog_modal
    )

    # Cargar proveedores
    load_suppliers()

# if __name__ == "__main__":
#     ft.app(target=home_page_proveedores)
