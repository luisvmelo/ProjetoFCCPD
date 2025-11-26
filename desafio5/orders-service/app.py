from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/orders')
def orders():
    pedidos = [
        {"id": 101, "produto": "Papel", "preco": 25},
        {"id": 102, "produto": "Caneta", "preco": 3},
        {"id": 103, "produto": "Caderno", "preco": 15}
    ]
    return jsonify(pedidos)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
