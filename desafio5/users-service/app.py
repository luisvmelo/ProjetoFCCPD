from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/users')
def users():
    usuarios = [
        {"id": 1, "nome": "Tiago", "email": "tiago@gmail.com"},
        {"id": 2, "nome": "Antonio", "email": "antonio@gmail.com"},
        {"id": 3, "nome": "Hugo", "email": "hugo@gmail.com"}
    ]
    return jsonify(usuarios)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
