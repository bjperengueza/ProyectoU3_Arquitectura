import requests
from flask import Blueprint, render_template, jsonify

orders_routes = Blueprint('orders_routes', __name__)

API_BASE_URL = 'http://localhost:4200/api/orders/details'

@orders_routes.route('/')
def list_orders():
    response = requests.get(API_BASE_URL)
    if response.status_code == 200:
        orders = response.json()
        print(orders)
        return render_template('order_details.html', orders=orders)
    else:
        return "Error fetching orders", response.status_code
