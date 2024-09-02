import requests
from flask import Blueprint, render_template, request, redirect, url_for, flash

proveedores_routes = Blueprint('proveedores_routes', __name__)

API_BASE_URL = 'http://localhost:4400/api/suppliers'

# Ruta para listar todos los proveedores
@proveedores_routes.route('/')
def list_suppliers():
    response = requests.get(API_BASE_URL)
    if response.status_code == 200:
        suppliers = response.json()
        return render_template('suppliers_list.html', suppliers=suppliers)
    else:
        flash("Error al obtener la lista de proveedores", "error")
        return render_template('suppliers_list.html', suppliers=[])

# Ruta para mostrar el formulario de crear un proveedor
@proveedores_routes.route('/create', methods=['GET', 'POST'])
def create_supplier():
    if request.method == 'POST':
        # Capturar los datos del formulario
        data = {
            'name': request.form['name'],
            'contact_name': request.form['contact_name'],
            'contact_email': request.form['contact_email'],
            'phone': request.form['phone'],
            'address': request.form['address']
        }
        # Realizar la petición POST para crear un proveedor
        response = requests.post(API_BASE_URL, json=data)
        if response.status_code == 201:
            flash("Proveedor creado exitosamente", "success")
            return redirect(url_for('proveedores_routes.list_suppliers'))
        else:
            flash("Error al crear el proveedor", "error")
    
    return render_template('supplier_form.html', action="Crear")

# Ruta para editar un proveedor
@proveedores_routes.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_supplier(id):
    if request.method == 'POST':
        # Capturar los datos del formulario
        data = {
            'name': request.form['name'],
            'contact_name': request.form['contact_name'],
            'contact_email': request.form['contact_email'],
            'phone': request.form['phone'],
            'address': request.form['address']
        }
        # Realizar la petición PUT para actualizar un proveedor
        response = requests.put(f'{API_BASE_URL}/{id}', json=data)
        if response.status_code == 200:
            flash("Proveedor actualizado exitosamente", "success")
            return redirect(url_for('proveedores_routes.list_suppliers'))
        else:
            flash("Error al actualizar el proveedor", "error")
    
    # Obtener los datos actuales del proveedor para pre-rellenar el formulario
    response = requests.get(f'{API_BASE_URL}/{id}')
    if response.status_code == 200:
        supplier = response.json()
        return render_template('supplier_form.html', supplier=supplier, action="Editar")
    else:
        flash("Error al obtener los datos del proveedor", "error")
        return redirect(url_for('proveedores_routes.list_suppliers'))

# Ruta para eliminar un proveedor
@proveedores_routes.route('/delete/<int:id>', methods=['POST'])
def delete_supplier(id):
    response = requests.delete(f'{API_BASE_URL}/{id}')
    if response.status_code == 200:
        flash("Proveedor eliminado exitosamente", "success")
    else:
        flash("Error al eliminar el proveedor", "error")
    
    return redirect(url_for('proveedores_routes.list_suppliers'))
