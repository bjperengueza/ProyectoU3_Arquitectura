import requests
from flask import Blueprint, render_template

dashboard_routes = Blueprint('dashboard_routes', __name__)

API_BASE_URL = 'http://localhost:4200/api/orders/count'
API_BASE_PRODUCTS = 'http://localhost:4200/api/products/count'
API_NUMERO_PROVEEDORES = 'http://localhost:4400/api/suppliers/count'
API_NUMERO_USUERS = 'http://localhost:4300/api/users/count'


@dashboard_routes.route('/')
def dashboard():
    # Solicitud para obtener el total de órdenes
    orders_response = requests.get(API_BASE_URL)
    
    if orders_response.status_code == 200:
        data_orders = orders_response.json()
        total_orders = data_orders.get('total_orders', 0)  # Si no existe 'total_orders', retorna 0
    else:
        total_orders = 0  # En caso de error con la API, mostrar 0

    # Solicitud para obtener el total de productos
    products_response = requests.get(API_BASE_PRODUCTS)
    
    if products_response.status_code == 200:
        data_products = products_response.json()
        total_products = data_products.get('total_products', 0)  # Si no existe 'total_products', retorna 0
    else:
        total_products = 0  # En caso de error con la API, mostrar 0
    
    suppliers_response = requests.get(API_NUMERO_PROVEEDORES)
    if suppliers_response.status_code == 200:
        data_suppliers = suppliers_response.json()
        total_suppliers = data_suppliers.get('total_suppliers',0)
    else:
        total_suppliers = 0
    
    users_response = requests.get(API_NUMERO_USUERS)
    if users_response.status_code == 200:
        data_users = users_response.json()
        total_users = data_users.get('total_users',0)

    # Pasamos ambos valores a la plantilla
    return render_template('dashboard.html', total_orders=total_orders, total_products=total_products, total_suppliers=total_suppliers, total_users=total_users)
