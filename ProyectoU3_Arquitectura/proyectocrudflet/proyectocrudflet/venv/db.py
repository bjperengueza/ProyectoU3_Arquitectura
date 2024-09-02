
# import mysql.connector

# def connect_db():
#     return mysql.connector.connect(
#         host="localhost",
#         user="root",
#         password="",
#         database="flet_crud_db"
#     )

import mysql.connector
from mysql.connector import Error
import requests
from werkzeug.security import check_password_hash, generate_password_hash

def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="flet_crud_db"
    )
    return connection


# #USUARIOS
# def authenticate_user(username, password):
#     connection = get_db_connection()
#     cursor = connection.cursor(dictionary=True)
#     cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
#     user = cursor.fetchone()
#     connection.close()
    
#     if user and check_password_hash(user['password'], password):
#         return user
#     return None
def authenticate_user(username, password):
    try:
        # Realizar una solicitud GET al endpoint de la API
        response = requests.get(f'http://localhost:4300/api/users/?username={username}')
        
        if response.status_code == 200:
            user_data = response.json()
            
            # Verificar que se encontró el usuario
            if user_data and 'password' in user_data:
                # Verificar la contraseña usando check_password_hash
                if check_password_hash(user_data['password'], password):
                    return user_data  # Retornar los datos del usuario si la autenticación es correcta
        else:
            print("Error al obtener los datos del usuario desde la API")
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con la API: {e}")
    
    return None  # Retornar None si la autenticación falla

def create_user(username, email, password):
    connection = get_db_connection()
    cursor = connection.cursor()
    hashed_password = generate_password_hash(password)
    cursor.execute(
        "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
        (username, email, hashed_password)
    )
    connection.commit()
    connection.close()
# create_user('jhonmacias1', 'jhonmacia1s1999@gmail.com', 'hola')


##CATEGORIAS
def get_categories():
    try:
        # Realizar una solicitud GET al endpoint de la API
        response = requests.get('http://localhost:4200/api/categories/')
        
        # Verificar si la solicitud fue exitosa
        if response.status_code == 200:
            # Retornar las categorías como lista de diccionarios
            return response.json()
        else:
            print(f"Error al obtener categorías: {response.status_code}")
            return []
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con la API: {e}")
        return []

def add_categories(name):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO categories (name) VALUES (%s)", (name,))
    connection.commit()
    connection.close()

def update_categories(categories_id, name):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE categories SET name = %s WHERE id = %s", (name, categories_id))
    connection.commit()
    connection.close()

def delete_categories(categories_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM categories WHERE id = %s", (categories_id,))
    connection.commit()
    connection.close()

def get_categories_by_id():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM categories")
    category = cursor.fetchone()
    connection.close()
    return category



#PRODUCTOS
def get_products():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    connection.close()
    return products

def add_product(name, description, price, quantity,iva,price_total,category_id,supplier_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO products (name, description, price, quantity,iva, price_total,category_id,supplier_id) VALUES (%s, %s, %s, %s,%s,%s,%s,%s)", (name, description, price, quantity,iva,price_total,category_id,supplier_id))
    connection.commit()
    connection.close()

def update_product(product_id, name, description, price, quantity):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE products SET name = %s, description = %s, price = %s, quantity = %s WHERE id = %s", (name, description, price, quantity, product_id))
    connection.commit()
    connection.close()

def delete_product(product_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
    connection.commit()
    connection.close()

def get_suppliers():
    try:
        # Realizar una solicitud GET al endpoint de la API
        response = requests.get('http://127.0.0.1:4400/api/suppliers/')
        
        # Verificar si la solicitud fue exitosa
        if response.status_code == 200:
            # Retornar los proveedores como lista de diccionarios
            return response.json()
        else:
            print(f"Error al obtener proveedores: {response.status_code}")
            return []
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con la API: {e}")
        return []
def add_suppliers(name, contact_name,contact_email, phone, address):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO suppliers (name, contact_name,contact_email, phone, address) VALUES (%s, %s, %s, %s,%s)", (name, contact_name,contact_email, phone, address))
    connection.commit()
    connection.close()

def update_suppliers(supplier_id, name, contact_name,contact_email, phone, address):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE suppliers SET name = %s, contact_name = %s, contact_email = %s, phone = %s WHERE id = %s", (name, contact_name,contact_email, phone, address, supplier_id))
    connection.commit()
    connection.close()

def delete_suppliers(supplier_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM suppliers WHERE id = %s", (supplier_id,))
    connection.commit()
    connection.close()