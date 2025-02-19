from database.db import get_connection, release_connection
from .entities.Usuario import Usuario
from utils.security import hash_password
import re
import bleach
from psycopg2.errors import UniqueViolation

class UsuarioModel:

    @classmethod
    def get_usuarios(cls):
        """ Obtiene todos los usuarios de la base de datos. """
        try:
            connection = get_connection()
            usuarios = []

            with connection.cursor() as cursor:
                cursor.execute("SELECT id, username, email, first_name, last_name, phone_number, address, city, country, birthdate, is_seller, seller_rating, cars_sold, registration_date, last_login, is_active, is_admin FROM public.usuarios ORDER BY id ASC")
                resultset = cursor.fetchall()

                for usuario in resultset:
                    usuarios.append(Usuario(*usuario).to_JSON())

            return usuarios
        except Exception as e:
            print(f"Error en get_usuarios: {e}")
            return {"error": "Error al obtener los usuarios"}, 500
        finally:
            release_connection(connection)

    @classmethod
    def get_usuario(cls, id):
        """ Obtiene un usuario por su ID. """
        if not isinstance(id, int) or id <= 0:
            return {"error": "ID inválido"}, 400

        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute("SELECT id, username, email, first_name, last_name, phone_number, address, city, country, birthdate, is_seller, seller_rating, cars_sold, registration_date, last_login, is_active, is_admin FROM public.usuarios WHERE id=%s", (id,))
                usuario = cursor.fetchone()

                if usuario:
                    return Usuario(*usuario).to_JSON(), 200
                return {"message": "Usuario no encontrado"}, 404
        except Exception as e:
            print(f"Error en get_usuario: {e}")
            return {"error": "Error al obtener el usuario"}, 500
        finally:
            release_connection(connection)

    @classmethod
    def get_usuario_by_email(cls, email):
        """ Obtiene un usuario por su email. """
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(pattern, email):
            return {"error": "Correo electrónico inválido"}, 400

        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute("SELECT id, username, email, password_hash FROM public.usuarios WHERE email=%s", (email,))
                usuario = cursor.fetchone()

                if usuario:
                    return {
                        "id": usuario[0],
                        "username": usuario[1],
                        "email": usuario[2],
                        "password_hash": usuario[3]
                    }, 200
                return {"message": "Usuario no encontrado"}, 404
        except Exception as e:
            print(f"Error en get_usuario_by_email: {e}")
            return {"error": "Error interno al obtener el usuario"}, 500
        finally:
            release_connection(connection)

    @classmethod
    def add_usuario(cls, usuario):
        """ Agrega un nuevo usuario a la base de datos. """
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                password_hashed = hash_password(usuario.password_hash)

                usuario.username = bleach.clean(usuario.username) if usuario.username else None
                usuario.email = bleach.clean(usuario.email) if usuario.email else None

                cursor.execute("SELECT id FROM public.usuarios WHERE username = %s OR email = %s", (usuario.username, usuario.email))
                existing_user = cursor.fetchone()
                if existing_user:
                    return {"error": "El usuario o el email ya están registrados"}, 400

                cursor.execute("""
                    INSERT INTO public.usuarios (username, email, password_hash, first_name, last_name, phone_number, address, city, country, birthdate, is_seller, seller_rating, cars_sold, registration_date, last_login, is_active, is_admin)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (usuario.username, usuario.email, password_hashed, usuario.first_name, usuario.last_name, usuario.phone_number, usuario.address, usuario.city, usuario.country, usuario.birthdate, usuario.is_seller, usuario.seller_rating, usuario.cars_sold, usuario.registration_date, usuario.last_login, usuario.is_active, usuario.is_admin))

                if cursor.rowcount == 1:
                    connection.commit()
                    return {"message": "Usuario agregado exitosamente"}, 201
                return {"error": "No se pudo agregar el usuario"}, 500
        except UniqueViolation:
            return {"error": "El usuario o el email ya están registrados"}, 400
        except Exception as e:
            print(f"Error en add_usuario: {e}")
            return {"error": f"Error interno: {str(e)}"}, 500
        finally:
            release_connection(connection)
