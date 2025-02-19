import psycopg2
from psycopg2 import DatabaseError, pool
from decouple import config
 
# Crear un pool de conexiones
connection_pool = pool.SimpleConnectionPool(
    1, 20,
    database=config('PGSQL_DATABASE'),
    user=config('PGSQL_USER'),
    password=config('PGSQL_PASSWORD'),
    host=config('PGSQL_HOST'),
    port=config('PGSQL_PORT')
)

def get_connection():
    try:
        return connection_pool.getconn()
    except Exception as e:
        print(f"Error obtenido conexión: {e}")
        return None
    
def release_connection(conn):
    if conn:
        connection_pool.putconn(conn)
