import sqlite3
from datetime import datetime

conn = sqlite3.connect('/data/banco.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS registros (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT
    )
''')

timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
cursor.execute('INSERT INTO registros (timestamp) VALUES (?)', (timestamp,))
conn.commit()

cursor.execute('SELECT * FROM registros')
registros = cursor.fetchall()

print(f"\nRegistros no banco: {len(registros)}")
for row in registros:
    print(f"  ID: {row[0]} | {row[1]}")

conn.close()
