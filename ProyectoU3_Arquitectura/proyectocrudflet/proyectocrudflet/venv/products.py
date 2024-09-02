import flet as ft
import requests
from db import  get_categories, get_suppliers

API_URL = "http://127.0.0.1:4200/api/products/"

def get_products():
    response = requests.get(API_URL)
    if response.status_code == 200:
        return response.json()
    return []

def add_product(name, description, price, quantity, iva, price_total, category_id, supplier_id):
    product_data = {
        "name": name,
        "description": description,
        "price": price,
        "quantity": quantity,
        "iva": iva,
        "price_total": price_total,
        "category_id": category_id,
        "supplier_id": supplier_id
    }
    response = requests.post(API_URL, json=product_data)
    if response.status_code == 201:
        print("Producto agregado exitosamente")
    else:
        print("Error al agregar el producto")

def update_product(product_id, name, description, price, quantity):
    product_data = {
        "name": name,
        "description": description,
        "price": price,
        "quantity": quantity
    }
    response = requests.put(f"{API_URL}{product_id}", json=product_data)
    if response.status_code == 200:
        print("Producto actualizado exitosamente")
    else:
        print("Error al actualizar el producto")

def delete_product(product_id):
    response = requests.delete(f"{API_URL}{product_id}")
    if response.status_code == 200:
        print("Producto eliminado exitosamente")
    else:
        print("Error al eliminar el producto")

def home_page(page: ft.Page):
    editing_product_id = None 

    def load_products(search_query=""):
        items = []
        products = get_products()
        for product in products:
            if search_query.lower() in product['name'].lower():
                category = next((cat for cat in categories if cat['id'] == product['category_id']), None)
                category_name = category['name'] if category else "Sin categoría"
                item = ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Column(
                                controls=[
                                    ft.Text(product['name'], weight="bold"),
                                    ft.Text(f"Precio: {product['price']} - Cantidad: {product['quantity']} - Categoría: {category_name}")
                                ],
                                expand=True
                            ),
                            ft.Row(
                                controls=[
                                    ft.IconButton(
                                        icon=ft.icons.EDIT,
                                        on_click=lambda e, p=product: edit_product_handler(e, p)
                                    ),
                                    ft.IconButton(
                                        icon=ft.icons.DELETE,
                                        on_click=lambda e, p=product['id']: delete_product_handler(e, p)
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

        if not desc_field.value:
            desc_error.value = "La descripción no puede estar vacía."
            errors = True
        else:
            desc_error.value = ""

        if not price_field.value.replace('.', '', 1).isdigit():
            price_error.value = "El precio debe ser un número válido."
            errors = True
        else:
            price_error.value = ""

        if not quantity_field.value.isdigit():
            quantity_error.value = "La cantidad debe ser un número entero."
            errors = True
        else:
            quantity_error.value = ""

        page.update()
        return not errors

    def calculate_price_with_iva(price, iva):
        return price * (1 + iva / 100)

    def add_product_handler(e):
        if not validate_inputs():
            return

        if selected_category_id is None:
            print("Debe seleccionar una categoría antes de agregar el producto.")
            return

        if selected_supplier_id is None:
            print("Debe seleccionar un proveedor antes de agregar el producto.")
            return

        category_id = selected_category_id
        supplier_id = selected_supplier_id

        # Calcular precio con IVA
        price = float(price_field.value)
        price_with_iva = calculate_price_with_iva(price, selected_iva)

        if editing_product_id:
            update_product(editing_product_id, name_field.value, desc_field.value, price, int(quantity_field.value))
        else:
            add_product(name_field.value, desc_field.value, price, int(quantity_field.value), selected_iva, price_with_iva, category_id, supplier_id)

        load_products(search_field.value)
        reset_form()
        dialog_modal.open = False
        page.update()

    def edit_product_handler(e, product):
        nonlocal editing_product_id
        editing_product_id = product['id']
        name_field.value = product['name']
        desc_field.value = product['description']
        price_field.value = str(product['price'])
        quantity_field.value = str(product['quantity'])
        dialog_modal.title.value = "Editar Producto"
        dialog_modal.actions[0].text = "Guardar Cambios"
        dialog_modal.open = True
        page.update()

    def delete_product_handler(e, product_id):
        delete_product(product_id)
        load_products(search_field.value)

    def search_handler(e):
        load_products(search_field.value)

    def logout_handler(e):
        page.show_login_page()

    def open_category_search(e):
        category_sheet.open = True
        page.update()

    def open_supplier_search(e):
        supplier_sheet.open = True
        page.update()

    def select_category(e):
        nonlocal selected_category_id
        selected_category_id = e.control.data
        selected_category_name = next((cat['name'] for cat in categories if cat['id'] == selected_category_id), "")
        category_text_field.value = selected_category_name
        category_sheet.open = False
        page.update()

    def select_supplier(e):
        nonlocal selected_supplier_id
        selected_supplier_id = e.control.data
        selected_supplier_name = next((sup['name'] for sup in suppliers if sup['id'] == selected_supplier_id), "")
        supplier_text_field.value = selected_supplier_name
        supplier_sheet.open = False
        page.update()

    def select_iva(e):
        nonlocal selected_iva
        selected_iva = float(e.control.value)
        page.update()

    def open_product_dialog(e):
        reset_form()  # Asegurarse de que el formulario esté limpio
        dialog_modal.title.value = "Agregar Producto"
        dialog_modal.actions[0].text = "Agregar Producto"
        dialog_modal.open = True
        page.update()

    def reset_form():
        nonlocal editing_product_id
        editing_product_id = None
        name_field.value = ""
        desc_field.value = ""
        price_field.value = ""
        quantity_field.value = ""
        category_text_field.value = ""
        supplier_text_field.value = ""
        selected_category_id = None
        selected_supplier_id = None
        page.update()

    # Obtener todas las categorías y proveedores
    categories = get_categories()
    suppliers = get_suppliers()

    # Inicializa las variables para almacenar las selecciones
    selected_category_id = None
    selected_supplier_id = None
    selected_iva = 0  # IVA predeterminado 0%

    # Campos de texto del formulario con iconos y validaciones
    name_field = ft.TextField(
        label="Nombre",
        prefix_icon=ft.icons.LABEL,
        on_change=lambda e: validate_inputs()
    )
    name_error = ft.Text("", color=ft.colors.RED)

    desc_field = ft.TextField(
        label="Descripción",
        prefix_icon=ft.icons.DESCRIPTION,
        on_change=lambda e: validate_inputs()
    )
    desc_error = ft.Text("", color=ft.colors.RED)

    price_field = ft.TextField(
        label="Precio",
        prefix_icon=ft.icons.ATTACH_MONEY,
        on_change=lambda e: validate_inputs()
    )
    price_error = ft.Text("", color=ft.colors.RED)

    quantity_field = ft.TextField(
        label="Cantidad",
        prefix_icon=ft.icons.SHOPPING_CART,
        on_change=lambda e: validate_inputs()
    )
    quantity_error = ft.Text("", color=ft.colors.RED)

    category_text_field = ft.TextField(
        label="Categoría",
        prefix_icon=ft.icons.CATEGORY,
        read_only=True
    )
    supplier_text_field = ft.TextField(
        label="Proveedor",
        prefix_icon=ft.icons.LOCAL_SHIPPING,
        read_only=True
    )

    # Bottom sheet para selección de categoría
    category_sheet = ft.BottomSheet(
        content=ft.Column(
            controls=[
                ft.ListTile(title=ft.Text(cat['name']), on_click=select_category, data=cat['id'])
                for cat in categories
            ],
        ),
        open=False
    )

    # Bottom sheet para selección de proveedor
    supplier_sheet = ft.BottomSheet(
        content=ft.Column(
            controls=[
                ft.ListTile(title=ft.Text(sup['name']), on_click=select_supplier, data=sup['id'])
                for sup in suppliers
            ],
        ),
        open=False
    )

    iva_dropdown = ft.Dropdown(
        label="Seleccionar IVA",
        options=[
            ft.dropdown.Option("0", text="0%"),
            ft.dropdown.Option("12", text="12%"),
            ft.dropdown.Option("15", text="15%")
        ],
        on_change=select_iva
    )

    # Diálogo para agregar y editar productos con scroll habilitado
    dialog_modal = ft.AlertDialog(
        title=ft.Text("Agregar Producto"),
        content=ft.Container(
            content=ft.Column(
                controls=[
                    name_field,
                    name_error,
                    desc_field,
                    desc_error,
                    price_field,
                    price_error,
                    quantity_field,
                    quantity_error,
                    iva_dropdown,
                    category_text_field,
                    ft.ElevatedButton(text="Seleccionar Categoría", on_click=open_category_search),
                    supplier_text_field,
                    ft.ElevatedButton(text="Seleccionar Proveedor", on_click=open_supplier_search),
                ],
                scroll=True  # Habilita el scroll dentro del formulario
            ),
            width=400,
            padding=20
        ),
        actions=[
            ft.TextButton("Agregar Producto", on_click=add_product_handler),
            ft.TextButton("Cancelar", on_click=lambda e: close_product_dialog(e))
        ],
        open=False
    )

    def close_product_dialog(e):
        dialog_modal.open = False
        reset_form()
        page.update()

    # Campo de búsqueda
    search_field = ft.TextField(label="Buscar Producto", prefix_icon=ft.icons.SEARCH, on_change=search_handler)
    search_button = ft.ElevatedButton(text="Buscar", on_click=search_handler, icon=ft.icons.SEARCH)

    # Botón para abrir el diálogo de productos
    dialog_button = ft.ElevatedButton(text="Agregar Producto", on_click=open_product_dialog, icon=ft.icons.ADD)

    # Botón de cerrar sesión
    logout_button = ft.ElevatedButton(text="Cerrar Sesión", on_click=logout_handler, icon=ft.icons.LOGOUT)

    # Lista de productos
    list_view = ft.ListView(
        auto_scroll=True,
        width=600,
        height=400
    )

    # Añadir los controles a la página
    page.add(
        search_field,
        search_button,
        dialog_button,
        list_view,
        logout_button,
        category_sheet,
        supplier_sheet,
        dialog_modal
    )

    # Cargar productos
    load_products()

# if __name__ == "__main__":
#     ft.app(target=home_page)
