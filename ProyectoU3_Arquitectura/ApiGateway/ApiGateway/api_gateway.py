from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Diccionario que mapea los nombres de los servicios a sus URLs
MICROSERVICES = {
    'products': 'http://127.0.0.1:4200/api/products',
    'categories': 'http://127.0.0.1:4200/api/categories',
    'orders': 'http://127.0.0.1:4200/api/orders',
    'users': 'http://127.0.0.1:4200/api/users',
    'suppliers': 'http://127.0.0.1:4200/api/suppliers',  # Si tienes esta ruta
    'dashboard': 'http://127.0.0.1:4600/dashboard'
}

@app.route('/api/<service_name>/', methods=['GET', 'POST'])
@app.route('/api/<service_name>/<path:endpoint>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def api_gateway(service_name, endpoint=''):
    if service_name not in MICROSERVICES:
        return jsonify({"error": "Service not found"}), 404

    # Construir la URL del servicio
    service_url = f"{MICROSERVICES[service_name]}"
    if endpoint:
        service_url = f"{service_url}/{endpoint}"

    try:
        if request.method == 'GET':
            response = requests.get(service_url, params=request.args)
        elif request.method == 'POST':
            headers = {'Content-Type': 'application/json'}
            response = requests.post(service_url, json=request.json, headers=headers)
        elif request.method == 'PUT':
            headers = {'Content-Type': 'application/json'}
            response = requests.put(service_url, json=request.json, headers=headers)
        elif request.method == 'DELETE':
            response = requests.delete(service_url, params=request.args)
        
        # Devolver la respuesta del microservicio
        response.raise_for_status()
        return jsonify(response.json()), response.status_code
    
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500
    except ValueError:
        return jsonify({"error": "Invalid JSON response"}), 500

if __name__ == '__main__':
    app.run(port=8080, debug=True)
