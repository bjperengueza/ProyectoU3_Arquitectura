from flask import Blueprint, request, jsonify
from models import Supplier, db

supplier_routes = Blueprint('supplier_routes', __name__)

# Obtener todos los proveedores
@supplier_routes.route('/', methods=['GET'])
def get_all_suppliers():
    suppliers = Supplier.query.all()
    return jsonify([{
        'id': supplier.id,
        'name': supplier.name,
        'contact_name': supplier.contact_name,
        'contact_email': supplier.contact_email,
        'phone': supplier.phone,
        'address': supplier.address
    } for supplier in suppliers])

# Obtener un proveedor por su ID
@supplier_routes.route('/<int:id>', methods=['GET'])
def get_supplier(id):
    supplier = Supplier.query.get(id)
    if supplier is None:
        return jsonify({'error': 'Supplier not found'}), 404
    return jsonify({
        'id': supplier.id,
        'name': supplier.name,
        'contact_name': supplier.contact_name,
        'contact_email': supplier.contact_email,
        'phone': supplier.phone,
        'address': supplier.address
    })

# Crear un nuevo proveedor
@supplier_routes.route('/', methods=['POST'])
def create_supplier():
    data = request.json
    new_supplier = Supplier(
        name=data['name'],
        contact_name=data['contact_name'],
        contact_email=data['contact_email'],
        phone=data['phone'],
        address=data['address']
    )
    db.session.add(new_supplier)
    db.session.commit()
    return jsonify({'message': 'Supplier created'}), 201

# Actualizar un proveedor existente
@supplier_routes.route('/<int:id>', methods=['PUT'])
def update_supplier(id):
    data = request.json
    supplier = Supplier.query.get(id)
    if supplier is None:
        return jsonify({'error': 'Supplier not found'}), 404
    
    supplier.name = data.get('name', supplier.name)
    supplier.contact_name = data.get('contact_name', supplier.contact_name)
    supplier.contact_email = data.get('contact_email', supplier.contact_email)
    supplier.phone = data.get('phone', supplier.phone)
    supplier.address = data.get('address', supplier.address)

    db.session.commit()
    return jsonify({'message': 'Supplier updated'})

# Eliminar un proveedor
@supplier_routes.route('/<int:id>', methods=['DELETE'])
def delete_supplier(id):
    supplier = Supplier.query.get(id)
    if supplier is None:
        return jsonify({'error': 'Supplier not found'}), 404
    
    db.session.delete(supplier)
    db.session.commit()
    return jsonify({'message': 'Supplier deleted'})
