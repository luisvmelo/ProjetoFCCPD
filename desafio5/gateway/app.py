from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route('/users')
def users():
    try:
        response = requests.get('http://users-service:5000/users')
        return response.json()
    except requests.exceptions.ConnectionError:
        return jsonify({"erro": "Servico de usuarios indisponivel"}), 503

@app.route('/orders')
def orders():
    try:
        response = requests.get('http://orders-service:5000/orders')
        return response.json()
    except requests.exceptions.ConnectionError:
        return jsonify({"erro": "Servico de pedidos indisponivel"}), 503

@app.route('/')
def index():
    return jsonify({
        "mensagem": "API Gateway",
        "rotas_disponiveis": [
            "GET /users - Lista usuarios",
            "GET /orders - Lista pedidos"
        ]
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
