from database.db import get_connection, release_connection
from .entities.Usuario import Usuario
from utils.security import hash_password
import re
import bleach
from psycopg2.errors import UniqueViolation

class UsuarioModel:

    @classmethod
    def get_usuarios(cls):
        try:
            connection = get_connection()
            usuarios = []

            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM public.usuarios ORDER BY id ASC")
                resultset = cursor.fetchall()

                for usuario in resultset:
                    user = Usuario(*usuario)
                    usuarios.append(user.to_JSON())

            connection.close()
            return usuarios
        except Exception as e:
            print(f"Error en get_usuarios: {e}")
            return {"error": "Error al obtener los usuarios"}
        finally:
            release_connection(connection)

    @classmethod
    def get_usuario(cls, id):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM public.usuarios WHERE id=%s", (id,))
                usuario = cursor.fetchone()

                user = None
                if usuario is not None:
                    user = Usuario(*usuario).to_JSON()

            connection.close()
            return user
        except Exception as e:
            print(f"Error en get_usuario: {e}")
            return {"error": "Error al obtener el usuario"}
        finally:
            release_connection(connection)

    @classmethod
    def get_usuario_by_email(cls, email):
        try:
            connection = get_connection()

            def is_valid_email(email):
                pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
                return re.match(pattern, email) is not None

            if not is_valid_email(email):
                return {"error": "Correo electrónico inválido"}  # Si el email no es válido
            
            with connection.cursor() as cursor:
                cursor.execute("SELECT id, username, email, password_hash FROM public.usuarios WHERE email=%s", (email,))
                usuario = cursor.fetchone()

                if usuario:
                    return {
                        "id": usuario[0],
                        "username": usuario[1],
                        "email": usuario[2],
                        "password_hash": usuario[3]
                    }
                return None  # Si el usuario no existe
        except Exception as e:
            print(f"Error en get_usuario_by_email: {e}")
            return None
        finally:
            release_connection(connection)


    

    @classmethod
    def add_usuario(cls, usuario):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                password_hashed = hash_password(usuario.password_hash)

                usuario.username = bleach.clean(usuario.username) if usuario.username else None
                usuario.email = bleach.clean(usuario.email) if usuario.email else None
                usuario.first_name = bleach.clean(usuario.first_name) if usuario.first_name else None
                usuario.last_name = bleach.clean(usuario.last_name) if usuario.last_name else None
                usuario.phone_number = bleach.clean(usuario.phone_number) if usuario.phone_number else None
                usuario.address = bleach.clean(usuario.address) if usuario.address else None
                usuario.city = bleach.clean(usuario.city) if usuario.city else None
                usuario.country = bleach.clean(usuario.country) if usuario.country else None

                birthdate = usuario.birthdate if usuario.birthdate else None
                is_seller = usuario.is_seller if usuario.is_seller is not None else False
                seller_rating = float(usuario.seller_rating) if usuario.seller_rating is not None else 0.0
                cars_sold = usuario.cars_sold if usuario.cars_sold is not None else 0
                registration_date = usuario.registration_date if usuario.registration_date else None
                last_login = usuario.last_login if usuario.last_login else None
                is_active = usuario.is_active if usuario.is_active is not None else True
                is_admin = usuario.is_admin if usuario.is_admin is not None else False

                cursor.execute("""INSERT INTO public.usuarios (username, email, password_hash, first_name, last_name, phone_number, address, city, country, birthdate, is_seller, seller_rating, cars_sold, registration_date, last_login, is_active, is_admin)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                            (usuario.username, usuario.email, password_hashed, usuario.first_name, usuario.last_name, usuario.phone_number, usuario.address, usuario.city, usuario.country, birthdate, is_seller, seller_rating, cars_sold, registration_date, last_login, is_active, is_admin))
                connection.commit()

            connection.close()
            return {"message": "Usuario agregado exitosamente"}

        except UniqueViolation as e:
            print(f"Error: {e}")
            return {"error": "El usuario o el email ya están registrados"}, 400

        except Exception as e:
            print(f"Error en add_usuario: {e}")
            return {"error": str(e)}, 500

        finally:
            release_connection(connection)


    @classmethod
    def delete_usuario(cls, id):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM public.usuarios WHERE id = %s", (id,))
                affected_rows = cursor.rowcount
                connection.commit()

            connection.close()
            return affected_rows
        except Exception as e:
            print(f"Error en delete_usuario: {e}")
            return {"error": "Error al eliminar el usuario"}
        finally:
            release_connection(connection)

    @classmethod
    def update_usuario(cls, usuario):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute("""UPDATE public.usuarios SET username=%s, email=%s, password_hash=%s, first_name=%s, last_name=%s, phone_number=%s, address=%s, city=%s, country=%s, birthdate=%s, is_seller=%s, seller_rating=%s, cars_sold=%s, registration_date=%s, last_login=%s, is_active=%s, is_admin=%s
                               WHERE id = %s""",
                               (usuario.username, usuario.email, usuario.password_hash, usuario.first_name, usuario.last_name, usuario.phone_number, usuario.address, usuario.city, usuario.country, usuario.birthdate, usuario.is_seller, usuario.seller_rating, usuario.cars_sold, usuario.registration_date, usuario.last_login, usuario.is_active, usuario.is_admin, usuario.id))
                affected_rows = cursor.rowcount
                connection.commit()

            connection.close()
            return affected_rows
        except Exception as e:
            print(f"Error en update_usuario: {e}")
            return {"error": "Error al actualizar el usuario"}
        finally:
            release_connection(connection)
