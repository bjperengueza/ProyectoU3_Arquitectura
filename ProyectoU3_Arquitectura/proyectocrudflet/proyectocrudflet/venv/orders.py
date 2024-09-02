import datetime
import flet as ft
import requests
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image
import re
import qrcode
from io import BytesIO

API_ORDERS_URL = "http://127.0.0.1:4200/api/orders/"
API_ORDERS_DETAILS_URL = "http://127.0.0.1:4200/api/orders/details"
API_PRODUCTS_URL = "http://127.0.0.1:4200/api/products/"
API_USERS_URL = "http://127.0.0.1:4300/api/users/"

def get_orders():
    response = requests.get(API_ORDERS_URL)
    if response.status_code == 200:
        return response.json()
    return []

def get_order_details():
    response = requests.get(API_ORDERS_DETAILS_URL)
    if response.status_code == 200:
        return response.json()
    return []

def get_products():
    response = requests.get(API_PRODUCTS_URL)
    if response.status_code == 200:
        return response.json()
    return []

def get_users():
    response = requests.get(API_USERS_URL)
    if response.status_code == 200:
        return response.json()
    return []

def format_date(date_string):
    # Detectar el formato de la fecha
    try:
        # Intentar analizar el formato "%Y-%m-%d" (por ejemplo: "2024-08-15")
        date_obj = datetime.datetime.strptime(date_string, "%Y-%m-%d")
    except ValueError:
        # Si falla, intentar analizar el formato "%a, %d %b %Y %H:%M:%S GMT"
        date_obj = datetime.datetime.strptime(date_string, "%a, %d %b %Y %H:%M:%S GMT")
    
    # Formatear la fecha en el formato deseado: "22 - AGOSTO - 2024"
    return date_obj.strftime("%d - %B - %Y").upper()


def add_order(product_id, user_id, order_date):
    order_data = {
        "product_id": product_id,
        "user_id": user_id,
        "order_date": order_date
    }
    response = requests.post(API_ORDERS_URL, json=order_data)
    if response.status_code == 201:
        print("Orden agregada exitosamente")
    else:
        print("Error al agregar la orden")

def update_order(order_id, product_id, user_id, order_date):
    order_data = {
        "product_id": product_id,
        "user_id": user_id,
        "order_date": order_date
    }
    response = requests.put(f"{API_ORDERS_URL}{order_id}", json=order_data)
    if response.status_code == 200:
        print("Orden actualizada exitosamente")
    else:
        print("Error al actualizar la orden")

def delete_order(order_id):
    response = requests.delete(f"{API_ORDERS_URL}{order_id}")
    if response.status_code == 200:
        print("Orden eliminada exitosamente")
    else:
        print("Error al eliminar la orden")

def sanitize_filename(filename):
    # Reemplaza caracteres no válidos en el nombre del archivo por guiones bajos
    return re.sub(r'[^\w\-_\. ]', '_', filename)

def generate_qr_code(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convertir la imagen en un objeto de bytes para insertarla en el PDF
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    buffered.seek(0)
    return buffered

def generate_pdf_report(order):
    sanitized_date = sanitize_filename(order['order_date'])
    file_name = f"Reporte_Orden_{sanitized_date}.pdf"
    doc = SimpleDocTemplate(file_name, pagesize=letter)
    elements = []

    # Estilo para la tabla
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#007BFF")),  # Color de fondo para la cabecera
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),  # Color del texto en la cabecera
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Alineación del texto
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Fuente para la cabecera
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Espaciado inferior en la cabecera
        ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),  # Color de fondo para el contenido
        ('GRID', (0, 0), (-1, -1), 1, colors.black)  # Bordes de la tabla
    ])

    # Datos para la tabla
    data = [
        ["Campo", "Valor"],  # Cabecera
        ["Producto", order['product_name']],
        ["Usuario", order['user_name']],
        ["Fecha", order['order_date']],
        ["Precio", order['product_price']],
        ["IVA", f"{order['product_iva']}%"],
        ["Precio Total", order['product_total_price']]
    ]

    # Crear la tabla
    table = Table(data)
    table.setStyle(table_style)

    # Generar código QR con la información de la orden
    qr_data = f"Producto: {order['product_name']}\nUsuario: {order['user_name']}\nFecha: {order['order_date']}\nPrecio Total: {order['product_total_price']}"
    qr_image = generate_qr_code(qr_data)

    # Convertir la imagen del QR en un objeto compatible con reportlab
    qr_img = Image(qr_image)
    qr_img.drawHeight = 100  # Ajustar el tamaño del QR
    qr_img.drawWidth = 100

    # Añadir la tabla y el QR al documento
    elements.append(table)
    elements.append(qr_img)
    doc.build(elements)

    print(f"Reporte generado: {file_name}")

def orders_page(page: ft.Page):
    editing_order_id = None
    selected_order_date = None

    def load_orders(search_query=""):
        items = []
        orders = get_order_details()
        for order in orders:
            if search_query.lower() in order['product_name'].lower() or search_query.lower() in order['user_name'].lower():
                formatted_date = format_date(order['order_date'])
                item = ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Column(
                                controls=[
                                    ft.Text(f"Producto: {order['product_name']} - Usuario: {order['user_name']}", weight="bold"),
                                    ft.Text(f"Fecha: {formatted_date}"),
                                    ft.Text(f"Precio: {order['product_price']}"),
                                    ft.Text(f"IVA: {order['product_iva']}%"),
                                    ft.Text(f"Precio Total: {order['product_total_price']}")
                                ],
                                expand=True
                            ),
                            ft.IconButton(
                                icon=ft.icons.PICTURE_AS_PDF,
                                icon_color="red",
                                on_click=lambda e, o=order: generate_pdf_report(o)
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
        if not selected_product_id:
            product_error.value = "Debe seleccionar un producto."
            errors = True
        else:
            product_error.value = ""

        if not selected_user_id:
            user_error.value = "Debe seleccionar un usuario."
            errors = True
        else:
            user_error.value = ""

        if not selected_order_date:
            date_error.value = "Debe seleccionar una fecha."
            errors = True
        else:
            date_error.value = ""

        page.update()
        return not errors

    def add_order_handler(e):
        if not validate_inputs():
            return

        if editing_order_id:
            update_order(editing_order_id, selected_product_id, selected_user_id, selected_order_date)
        else:
            add_order(selected_product_id, selected_user_id, selected_order_date)

        load_orders(search_field.value)
        reset_form()
        dialog_modal.open = False
        page.update()

    def handle_date_change(e):
        nonlocal selected_order_date
        selected_order_date = e.control.value.strftime('%Y-%m-%d')
        order_date_field.value = selected_order_date
        page.update()

    def handle_date_dismissal(e):
        page.add(ft.Text(f"DatePicker dismissed"))

    def edit_order_handler(e, order):
        nonlocal editing_order_id
        editing_order_id = order['id']
        product = next((prod for prod in products if prod['id'] == order['product_id']), None)
        user = next((usr for usr in users if usr['id'] == order['user_id']), None)
        selected_product_id = order['product_id']
        selected_user_id = order['user_id']
        product_text_field.value = product['name'] if product else "Producto no encontrado"
        user_text_field.value = user['name'] if user else "Usuario no encontrado"
        selected_order_date = order['order_date']
        order_date_field.value = selected_order_date
        dialog_modal.title.value = "Editar Orden"
        dialog_modal.actions[0].text = "Guardar Cambios"
        dialog_modal.open = True
        page.update()

    def delete_order_handler(e, order_id):
        delete_order(order_id)
        load_orders(search_field.value)

    def search_handler(e):
        load_orders(search_field.value)

    def open_product_search(e):
        product_sheet.open = True
        page.update()

    def open_user_search(e):
        user_sheet.open = True
        page.update()

    def select_product(e):
        nonlocal selected_product_id
        selected_product_id = e.control.data
        selected_product_name = next((prod['name'] for prod in products if prod['id'] == selected_product_id), "")
        product_text_field.value = selected_product_name
        product_sheet.open = False
        page.update()

    def select_user(e):
        nonlocal selected_user_id
        selected_user_id = e.control.data
        selected_user_name = next((usr['username'] for usr in users if usr['id'] == selected_user_id), "")
        user_text_field.value = selected_user_name
        user_sheet.open = False
        page.update()

    def open_order_dialog(e):
        reset_form()  # Asegurarse de que el formulario esté limpio
        dialog_modal.title.value = "Agregar Orden"
        dialog_modal.actions[0].text = "Agregar Orden"
        dialog_modal.open = True
        page.update()

    def reset_form():
        nonlocal editing_order_id, selected_order_date
        editing_order_id = None
        product_text_field.value = ""
        user_text_field.value = ""
        order_date_field.value = ""
        selected_product_id = None
        selected_user_id = None
        selected_order_date = None
        page.update()

    # Obtener todos los productos y usuarios
    products = get_products()
    users = get_users()

    # Inicializa las variables para almacenar las selecciones
    selected_product_id = None
    selected_user_id = None

    # Campos de texto del formulario con iconos y validaciones
    product_text_field = ft.TextField(
        label="Producto",
        prefix_icon=ft.icons.CATEGORY,
        read_only=True
    )
    product_error = ft.Text("", color=ft.colors.RED)

    user_text_field = ft.TextField(
        label="Usuario",
        prefix_icon=ft.icons.PERSON,
        read_only=True
    )
    user_error = ft.Text("", color=ft.colors.RED)

    order_date_field = ft.TextField(
        label="Fecha de Orden",
        prefix_icon=ft.icons.DATE_RANGE,
        read_only=True
    )
    date_error = ft.Text("", color=ft.colors.RED)

    # Bottom sheet para selección de producto
    product_sheet = ft.BottomSheet(
        content=ft.Column(
            controls=[
                ft.ListTile(title=ft.Text(prod['name']), on_click=select_product, data=prod['id'])
                for prod in products
            ],
        ),
        open=False
    )

    # Bottom sheet para selección de usuario
    user_sheet = ft.BottomSheet(
        content=ft.Column(
            controls=[
                ft.ListTile(title=ft.Text(usr['username']), on_click=select_user, data=usr['id'])
                for usr in users
            ],
        ),
        open=False
    )

    # Diálogo para agregar y editar órdenes
    dialog_modal = ft.AlertDialog(
        title=ft.Text("Agregar Orden"),
        content=ft.Container(
            content=ft.Column(
                controls=[
                    product_text_field,
                    product_error,
                    ft.ElevatedButton(text="Seleccionar Producto", on_click=open_product_search),
                    user_text_field,
                    user_error,
                    ft.ElevatedButton(text="Seleccionar Usuario", on_click=open_user_search),
                    order_date_field,
                    ft.ElevatedButton(
                        "Seleccionar Fecha",
                        icon=ft.icons.CALENDAR_MONTH,
                        on_click=lambda e: page.open(
                            ft.DatePicker(
                                first_date=datetime.datetime(year=2023, month=1, day=1),
                                last_date=datetime.datetime(year=2025, month=12, day=31),
                                on_change=handle_date_change,
                                on_dismiss=handle_date_dismissal,
                            )
                        ),
                    ),
                    date_error
                ],
                scroll=True  # Habilita el scroll dentro del formulario
            ),
            width=400,
            padding=20
        ),
        actions=[
            ft.TextButton("Agregar Orden", on_click=add_order_handler),
            ft.TextButton("Cancelar", on_click=lambda e: close_order_dialog(e))
        ],
        open=False
    )

    def close_order_dialog(e):
        dialog_modal.open = False
        reset_form()
        page.update()

    # Campo de búsqueda
    search_field = ft.TextField(label="Buscar Orden", prefix_icon=ft.icons.SEARCH, on_change=search_handler)
    search_button = ft.ElevatedButton(text="Buscar", on_click=search_handler, icon=ft.icons.SEARCH)

    # Botón para abrir el diálogo de órdenes
    dialog_button = ft.ElevatedButton(text="Agregar Orden", on_click=open_order_dialog, icon=ft.icons.ADD)

    # Botón de cerrar sesión
    logout_button = ft.ElevatedButton(text="Cerrar Sesión", on_click=lambda e: page.show_login_page(), icon=ft.icons.LOGOUT)

    # Lista de órdenes
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
        product_sheet,
        user_sheet,
        dialog_modal
    )

    # Cargar órdenes
    load_orders()

# if __name__ == "__main__":
#     ft.app(target=orders_page)
