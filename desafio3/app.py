from flask import Flask
import redis
import psycopg2
from datetime import datetime

app = Flask(__name__)

redis_client = redis.Redis(host='cache', port=6379, decode_responses=True)

@app.route('/')
def index():
    visitas = redis_client.incr('contador_visitas')

    try:
        conn = psycopg2.connect(
            host='db',
            database='postgres',
            user='postgres',
            password='senha123'
        )
        conn.close()
        db_status = "conectado"
    except:
        db_status = "offline"

    agora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    return f"""
    visitas: {visitas}
    postgres: {db_status}
    redis: ativo
    horario: {agora}
    """

@app.route('/reset')
def reset():
    redis_client.set('contador_visitas', 0)
    return "resetado"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
