import flet as ft
from products import home_page  # Importa la función products desde productos.py
from categories import home_page_categories
from proveedores import home_page_proveedores
from orders import orders_page
def navegation(page: ft.Page):
    page.title = "NavigationBar Example"
    
    # Define different modules or content for each navigation destination
    def show_products():
        page.controls.clear()
        home_page(page)  # Llama a la función products para mostrar el contenido de productos
        page.add(navigation_bar)
        page.update()

    def show_categories():
        page.controls.clear()
        home_page_categories(page)
        #page.add(ft.Text("Categorias"))
        page.add(navigation_bar)
        page.update()

    def show_suppliers():
        page.controls.clear()
        home_page_proveedores(page)
        # page.add(ft.Text("Proveedores"))
        page.add(navigation_bar)
        page.update()
        
    def show_orders():
        page.controls.clear()
        orders_page(page)
        #page.add(ft.Text("Ordenes"))
        page.add(navigation_bar)
        page.update()

    # Event handler for navigation bar item selection
    def on_navigation(index):
        if index == 0:
            show_products()
        elif index == 1:
            show_categories()
        elif index == 2:
            show_suppliers()
        elif index == 3:
            show_orders()

    # Create the navigation bar with destinations
    navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.icons.EXPLORE, label="Productos"),
            ft.NavigationBarDestination(icon=ft.icons.COMMUTE, label="Categorias"),
            ft.NavigationBarDestination(
                icon=ft.icons.BOOKMARK_BORDER,
                selected_icon=ft.icons.BOOKMARK,
                label="Proveedores",
            ),
             ft.NavigationBarDestination(
                icon=ft.icons.SHOPPING_CART,
                selected_icon=ft.icons.BOOKMARK,
                label="Ordenes",
            ),
        ],
        on_change=lambda e: on_navigation(e.control.selected_index)  # Bind the navigation bar's change event to the handler
    )

    # Initialize with the default module
    show_products()
