from database.db import get_connection, release_connection
from .entities.Usuario import Usuario
from utils.security import hash_password


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
    def add_usuario(cls, usuario):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                password_hashed = hash_password(usuario.password_hash) # Ciframos la contraseña
                cursor.execute("""INSERT INTO public.usuarios (username, email, password_hash, first_name, last_name, phone_number, address, city, country, birthdate, is_seller, seller_rating, cars_sold, registration_date, last_login, is_active, is_admin)
                               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                               (usuario.username, usuario.email, password_hashed, usuario.first_name, usuario.last_name, usuario.phone_number, usuario.address, usuario.city, usuario.country, usuario.birthdate, usuario.is_seller, usuario.seller_rating, usuario.cars_sold, usuario.registration_date, usuario.last_login, usuario.is_active, usuario.is_admin))
                connection.commit()

            connection.close()
            return {"message": "Usuario agregado exitosamente"}
        except Exception as e:
            print(f"Error en add_usuario: {e}")
            return {"error": "Error al agregar el usuario"}
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
