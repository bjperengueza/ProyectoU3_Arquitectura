from flask import Flask
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    from app.routes.product_routes import product_routes
    from app.routes.dash import dashboard_routes
    from app.routes.login import users_routes
    from app.routes.orders_route import orders_routes
    from app.routes.proveedores import proveedores_routes
    app.register_blueprint(product_routes, url_prefix='/products')
    app.register_blueprint(dashboard_routes, url_prefix='/dashboard')
    app.register_blueprint(users_routes, url_prefix='/usuarios')
    app.register_blueprint(orders_routes, url_prefix='/orders')
    app.register_blueprint(proveedores_routes, url_prefix='/suppliers')
    
    
    
    return app
