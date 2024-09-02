import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    API_BASE_URL = os.getenv('API_BASE_URL', 'http://localhost:4200/api/products')
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'clave_secreta_por_defecto_super_segura'

