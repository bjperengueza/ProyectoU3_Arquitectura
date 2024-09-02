import flet as ft
from db import get_categories  # Asumiendo que tienes esta función para obtener las categorías

def main(page: ft.Page):
    categories = get_categories()

    def close_anchor(e):
        selected_category = e.control.title.value
        category_text_field.value = selected_category
        category_text_field.update()
        anchor.close_view()
        print(f"Categoría seleccionada: {selected_category}")

    def handle_tap(e):
        print(f"handle_tap")

    anchor = ft.BottomSheet(
        content=ft.Column(
            controls=[
                ft.ListTile(title=ft.Text(cat['name']), on_click=close_anchor, data=cat['id'])
                for cat in categories
            ],
        ),
        open=False
    )

    category_text_field = ft.TextField(label="Categoría seleccionada")

    def open_category_search(e):
        anchor.open = True
        page.update()

    page.add(
        ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.OutlinedButton(
                    "Seleccionar Categoría",
                    on_click=open_category_search,
                ),
            ],
        ),
        category_text_field,
        anchor,
    )

# if __name__ == "__main__":
#     ft.app(target=main)
