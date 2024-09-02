from flask import Flask
from flask_cors import CORS  # Importa CORS
from routes.products import product_routes
from routes.categories import category_routes
from database import db
from routes.proveedores import supplier_routes
from routes.orders import order_routes
from routes.users import user_routes
app = Flask(__name__)

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@mysql-container/flet_crud_db'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/flet_crud_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Habilitar CORS para toda la aplicación
CORS(app, resources={r"/api/*": {"origins": "*"}})
# Inicializar base de datos
db.init_app(app)

# Registrar blueprints de rutas
app.register_blueprint(product_routes, url_prefix='/api/products')
app.register_blueprint(category_routes, url_prefix='/api/categories')
#app.register_blueprint(supplier_routes, url_prefix='/api/suppliers')  
app.register_blueprint(order_routes, url_prefix='/api/orders')  
app.register_blueprint(user_routes, url_prefix='/api/users')  




if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Crear tablas si no existen
    app.run(debug=True, port=4200)
