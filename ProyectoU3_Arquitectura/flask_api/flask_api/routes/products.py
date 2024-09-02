from flask import Blueprint, request, jsonify
from models import Product, db

product_routes = Blueprint('product_routes', __name__)

@product_routes.route('/', methods=['GET'])
def get_all_products():
    products = Product.query.all()
    return jsonify([{
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'price': product.price,
        'quantity':product.quantity,
        'category_id': product.category_id,
        'supplier_id':product.supplier_id,
        'iva':product.iva,
        'price_total':product.price_total
    } for product in products])

@product_routes.route('/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.query.get(id)
    if product is None:
        return jsonify({'error': 'Product not found'}), 404
    return jsonify({
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'price': product.price,
        'quantity':product.quantity,
        'category_id': product.category_id,
        'supplier_id':product.supplier_id,
        'iva':product.iva,
        'price_total':product.price_total
    })

@product_routes.route('/', methods=['POST'])
def create_product():
    data = request.json
    new_product = Product(
        name=data['name'],
        description=data.get('description', ''),
        price=data['price'],
        quantity =data['quantity'],
        category_id=data['category_id'],
        supplier_id=data['supplier_id'],
        iva = data['iva'],
        price_total=data['price_total']
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify({'message': 'Product created'}), 201

@product_routes.route('/<int:id>', methods=['PUT'])
def update_product(id):
    data = request.json
    product = Product.query.get(id)
    if product is None:
        return jsonify({'error': 'Product not found'}), 404
    
    product.name = data.get('name', product.name)
    product.description = data.get('description', product.description)
    product.price = data.get('price', product.price)
    product.category_id = data.get('category_id', product.category_id)
    product.iva = data.get('iva', product.iva)
    product.price_total = data.get('price_total', product.price_total)
    db.session.commit()
    return jsonify({'message': 'Product updated'})

@product_routes.route('/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get(id)
    if product is None:
        return jsonify({'error': 'Product not found'}), 404
    
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted'})

@product_routes.route('/count', methods=['GET'])
def count_orders():
    total_products = db.session.query(db.func.count(Product.id)).scalar()
    return jsonify({'total_products': total_products})


@product_routes.route('/count-by-iva', methods=['GET'])
def count_products_by_iva():
    results = db.session.query(Product.iva, db.func.count(Product.id)).group_by(Product.iva).all()
    data = {str(iva): count for iva, count in results}
    return jsonify(data)
