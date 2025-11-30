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
            resultado.append(f"{usuario['nome']} ativo")

        return '<br>'.join(resultado)
    except:
        return "service-a offline", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
