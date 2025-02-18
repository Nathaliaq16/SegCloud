import psycopg2
from psycopg2 import DatabaseError
from decouple import config

def get_connection():
    try:
        conn = psycopg2.connect(
            database=config('PGSQL_DATABASE'),
            user=config('PGSQL_USER'),
            password=config('PGSQL_PASSWORD'),
            host=config('PGSQL_HOST')
        )
        return conn
    except DatabaseError as e:
        print(e)
        return None
