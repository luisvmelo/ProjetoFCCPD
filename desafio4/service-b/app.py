from flask import Flask
import requests

app = Flask(__name__)

@app.route('/status')
def status():
    try:
        response = requests.get('http://service-a:5001/users')
        usuarios = response.json()

        resultado = []
        for usuario in usuarios:
            resultado.append(f"Usuário {usuario['nome']} está ativo")

        return '<br>'.join(resultado)

    except requests.exceptions.ConnectionError:
        return "Erro: Não foi possível conectar ao Service A", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
