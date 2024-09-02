from flask import Blueprint, request, jsonify
from models import User, db

user_routes = Blueprint('user_routes', __name__)

# Obtener todos los usuarios
@user_routes.route('/', methods=['GET'])
def get_all_users():
    users = User.query.all()
    return jsonify([{
        'id': user.id,
        'username': user.username,
        'password' : user.password,
        'email': user.email,
        'created_at': user.created_at
    } for user in users])

# Obtener un usuario por su ID
@user_routes.route('/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    if user is None:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({
        'id': user.id,
        'username': user.username,
        'password' : user.password,
        'email': user.email,
        'created_at': user.created_at
    })

# Crear un nuevo usuario
@user_routes.route('/', methods=['POST'])
def create_user():
    data = request.json
    if User.query.filter_by(username=data['username']).first() or User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Username or email already exists'}), 409

    new_user = User(
        username=data['username'],
        email=data['email']
    )
    new_user.set_password(data['password'])

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created'}), 201

# Actualizar un usuario existente
@user_routes.route('/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.json
    user = User.query.get(id)
    if user is None:
        return jsonify({'error': 'User not found'}), 404

    if 'username' in data:
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'error': 'Username already exists'}), 409
        user.username = data['username']

    if 'email' in data:
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already exists'}), 409
        user.email = data['email']

    if 'password' in data:
        user.set_password(data['password'])

    db.session.commit()
    return jsonify({'message': 'User updated'})

# Eliminar un usuario
@user_routes.route('/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if user is None:
        return jsonify({'error': 'User not found'}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted'})


@user_routes.route('/count', methods=['GET'])
def count_users():
    # Realizar la consulta para contar el número de órdenes
    total_users = db.session.query(db.func.count(User.id)).scalar()

    return jsonify({'total_users': total_users})
