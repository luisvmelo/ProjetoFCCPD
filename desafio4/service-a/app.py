from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/users')
def users():
    usuarios = [
        {"id": 1, "nome": "Luis"},
        {"id": 2, "nome": "Eduardo"},
        {"id": 3, "nome": "Mayla"}
    ]
    return jsonify(usuarios)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
