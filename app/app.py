import os
import time
from flask import Flask, jsonify, render_template_string
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

# Configuración mediante variables de entorno
APP_NAME = os.getenv("APP_NAME", "Flask DevOps App")
APP_VERSION = os.getenv("APP_VERSION", "2.0.0")
DB_HOST = os.getenv("DB_HOST", "db")
DB_NAME = os.getenv("DB_NAME", "mi_base_datos")
DB_USER = os.getenv("DB_USER", "usuario")
DB_PASSWORD = os.getenv("DB_PASSWORD", "contrasena")

def get_db_connection():
    """Intenta conectar a la base de datos con reintentos."""
    retries = 5
    while retries > 0:
        try:
            conn = psycopg2.connect(
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
            )
            return conn
        except psycopg2.OperationalError:
            retries -= 1
            time.sleep(2)
    return None

def init_db():
    """Crea la tabla e inserta datos iniciales si está vacía."""
    conn = get_db_connection()
    if conn:
        curr = conn.cursor()
        # Crear tabla
        curr.execute('''
            CREATE TABLE IF NOT EXISTS productos (
                id SERIAL PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                precio NUMERIC(10, 2) NOT NULL,
                stock INT NOT NULL
            );
        ''')
        # Verificar si ya hay datos
        curr.execute('SELECT COUNT(*) FROM productos;')
        if curr.fetchone()[0] == 0:
            productos_iniciales = [
                ('Laptop', 899.99, 15),
                ('Mouse Gamer', 45.50, 50),
                ('Teclado Mecánico', 89.00, 30),
                ('Monitor 24"', 150.00, 20),
                ('Auriculares', 60.00, 40)
            ]
            curr.executemany(
                'INSERT INTO productos (nombre, precio, stock) VALUES (%s, %s, %s);',
                productos_iniciales
            )
        conn.commit()
        curr.close()
        conn.close()

# Inicializar la base de datos al arrancar
init_db()

@app.route('/')
def index():
    conn = get_db_connection()
    db_status = "⚡ Conectado exitosamente" if conn else "❌ Error de conexión"
    if conn:
        conn.close()

    html = """
    <h1>Información del Sistema</h1>
    <p><strong>Aplicación:</strong> {{ app_name }}</p>
    <p><strong>Versión:</strong> {{ app_version }}</p>
    <p><strong>Estado de PostgreSQL:</strong> {{ db_status }}</p>
    <p><a href="/productos">Ver todos los productos</a></p>
    """
    return render_template_string(html, app_name=APP_NAME, app_version=APP_VERSION, db_status=db_status)

@app.route('/productos')
def get_productos():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "No se pudo conectar a la base de datos"}), 500
    
    curr = conn.cursor(cursor_factory=RealDictCursor)
    curr.execute('SELECT * FROM productos;')
    productos = curr.fetchall()
    curr.close()
    conn.close()
    return jsonify(productos)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)