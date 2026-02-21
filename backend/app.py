from flask import Flask, jsonify
import os
import psycopg2

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        host=os.environ.get('POSTGRES_HOST', 'db'),
        database=os.environ.get('POSTGRES_DB', 'testdb'),
        user=os.environ.get('POSTGRES_USER', 'postgres'),
        password=os.environ.get('POSTGRES_PASSWORD', 'postgres')
    )
    return conn

@app.route('/')
def index():
    return "Hello from Backend!"

@app.route('/users')
def users():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, name TEXT);')
    cur.execute("INSERT INTO users (name) VALUES ('Alice') ON CONFLICT DO NOTHING;")
    cur.execute('SELECT * FROM users;')
    users_list = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(users_list)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)