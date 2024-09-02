from flask import Blueprint, request, jsonify
from models import Order, db, Product, User
import datetime

order_routes = Blueprint('order_routes', __name__)

# Formatear la fecha a 'YYYY-MM-DD'
def format_date(date_obj):
    if isinstance(date_obj, (datetime.date, datetime.datetime)):
        return date_obj.strftime('%Y-%m-%d')
    return date_obj 


# Obtener todas las órdenes
@order_routes.route('/', methods=['GET'])
def get_all_orders():
    orders = Order.query.all()
    return jsonify([{
        'id': order.id,
        'product_id': order.product_id,
        'user_id': order.user_id,
        'order_date': format_date(order.order_date)
    } for order in orders])

# Obtener una orden por su ID
@order_routes.route('/<int:id>', methods=['GET'])
def get_order(id):
    order = Order.query.get(id)
    if order is None:
        return jsonify({'error': 'Order not found'}), 404
    return jsonify({
        'id': order.id,
        'product_id': order.product_id,
        'user_id': order.user_id,
        'order_date': format_date(order.order_date)
    })

# Crear una nueva orden
@order_routes.route('/', methods=['POST'])
def create_order():
    data = request.json
    new_order = Order(
        product_id=data['product_id'],
        user_id=data['user_id'],
        order_date=data['order_date']
    )
    db.session.add(new_order)
    db.session.commit()
    return jsonify({'message': 'Order created'}), 201

# Actualizar una orden existente
@order_routes.route('/<int:id>', methods=['PUT'])
def update_order(id):
    data = request.json
    order = Order.query.get(id)
    if order is None:
        return jsonify({'error': 'Order not found'}), 404
    
    order.product_id = data.get('product_id', order.product_id)
    order.user_id = data.get('user_id', order.user_id)
    order.order_date = data.get('order_date', order.order_date)
    
    db.session.commit()
    return jsonify({'message': 'Order updated'})

# Eliminar una orden
@order_routes.route('/<int:id>', methods=['DELETE'])
def delete_order(id):
    order = Order.query.get(id)
    if order is None:
        return jsonify({'error': 'Order not found'}), 404
    
    db.session.delete(order)
    db.session.commit()
    return jsonify({'message': 'Order deleted'})

# Obtener detalles de órdenes con productos y usuarios, además de precio, IVA y total
@order_routes.route('/details', methods=['GET'])
def get_order_details():
    # Realizar la consulta usando SQLAlchemy
    results = db.session.query(
        Order.order_date,
        Product.name.label('product_name'),
        Product.price.label('product_price'),
        Product.iva.label('product_iva'),
        Product.price_total.label('product_total_price'),
        User.username.label('user_name')
    ).join(Product, Order.product_id == Product.id)\
     .join(User, Order.user_id == User.id).all()

    # Convertir los resultados en una lista de diccionarios
    order_details = [{
        'order_date': format_date(result.order_date),
        'product_name': result.product_name,
        'product_price': result.product_price,
        'product_iva': result.product_iva,
        'product_total_price': result.product_total_price,
        'user_name': result.user_name
    } for result in results]

    return jsonify(order_details)

@order_routes.route('/count', methods=['GET'])
def count_orders():
    # Realizar la consulta para contar el número de órdenes
    total_orders = db.session.query(db.func.count(Order.id)).scalar()

    return jsonify({'total_orders': total_orders})
