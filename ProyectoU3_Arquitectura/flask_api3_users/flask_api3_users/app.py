from flask import Flask
from database import db
from routes.users import user_routes
app = Flask(__name__)

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@mysql-container/flet_crud_db'

#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/flet_crud_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
app.register_blueprint(user_routes, url_prefix='/api/users')  




if __name__ == "__main__":
    with app.app_context():
        db.create_all() 
    app.run(debug=True, port=4300)
