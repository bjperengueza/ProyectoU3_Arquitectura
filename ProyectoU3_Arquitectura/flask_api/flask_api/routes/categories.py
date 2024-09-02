from flask import Blueprint, request, jsonify
from models import Category, db

category_routes = Blueprint('category_routes', __name__)

@category_routes.route('/', methods=['GET'])
def get_all_categories():
    categories = Category.query.all()
    return jsonify([{
        'id': category.id,
        'name': category.name
    } for category in categories])

@category_routes.route('/<int:id>', methods=['GET'])
def get_category(id):
    category = Category.query.get(id)
    if category is None:
        return jsonify({'error': 'Category not found'}), 404
    return jsonify({
        'id': category.id,
        'name': category.name
    })

@category_routes.route('/', methods=['POST'])
def create_category():
    data = request.json
    new_category = Category(name=data['name'])
    db.session.add(new_category)
    db.session.commit()
    return jsonify({'message': 'Category created'}), 201

@category_routes.route('/<int:id>', methods=['PUT'])
def update_category(id):
    data = request.json
    category = Category.query.get(id)
    if category is None:
        return jsonify({'error': 'Category not found'}), 404
    
    category.name = data.get('name', category.name)
    db.session.commit()
    return jsonify({'message': 'Category updated'})

@category_routes.route('/<int:id>', methods=['DELETE'])
def delete_category(id):
    category = Category.query.get(id)
    if category is None:
        return jsonify({'error': 'Category not found'}), 404
    
    db.session.delete(category)
    db.session.commit()
    return jsonify({'message': 'Category deleted'})
