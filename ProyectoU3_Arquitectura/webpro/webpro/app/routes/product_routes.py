import requests
from flask import Blueprint, render_template, jsonify

product_routes = Blueprint('product_routes', __name__)

API_BASE_URL = 'http://localhost:4200/api/products'

@product_routes.route('/')
def list_products():
    response = requests.get(API_BASE_URL)
    if response.status_code == 200:
        products = response.json()
        #print(products)
        return render_template('product_list.html', products=products)
    else:
        return "Error fetching products", response.status_code

@product_routes.route('/<int:id>')
def get_product(id):
    response = requests.get(f'{API_BASE_URL}/{id}')
    if response.status_code == 200:
        product = response.json()
        return render_template('product_detail.html', product=product)
    else:
        return "Product not found", response.status_code
