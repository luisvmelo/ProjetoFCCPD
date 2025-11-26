from flask import Flask
import redis
import psycopg2
from datetime import datetime

app = Flask(__name__)

redis_client = redis.Redis(host='cache', port=6379, decode_responses=True)

@app.route('/')
def index():
    visitas = redis_client.incr('contador_visitas')

    db_status = "ERRO"
    try:
        conn = psycopg2.connect(
            host='db',
            database='postgres',
            user='postgres',
            password='senha123'
        )
        conn.close()
        db_status = "CONECTADO"
    except Exception as e:
        db_status = f"ERRO: {str(e)}"

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    response = f"""
    ======================================
    Sistema Multi-Serviços (Docker Compose)
    ======================================

    Contador de Visitas: {visitas}
    Status PostgreSQL: {db_status}
    Cache Redis: ATIVO
    Timestamp: {timestamp}

    ======================================
    Recarregue a página para incrementar!
    ======================================
    """

    return response

@app.route('/reset')
def reset():
    redis_client.set('contador_visitas', 0)
    return "Contador resetado! Volte para / para testar."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
