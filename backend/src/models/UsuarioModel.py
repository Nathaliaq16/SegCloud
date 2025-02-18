from database.db import get_connection
from .entities.Usuario import Usuario


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
            return Exception(e)

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
            return Exception(e)

    @classmethod
    def add_usuario(cls, usuario):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute("""INSERT INTO public.usuarios (username, email, password_hash, first_name, last_name, phone_number, address, city, country, birthdate, is_seller, seller_rating, cars_sold, registration_date, last_login, is_active, is_admin)
                               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                               (usuario.username, usuario.email, usuario.password_hash, usuario.first_name, usuario.last_name, usuario.phone_number, usuario.address, usuario.city, usuario.country, usuario.birthdate, usuario.is_seller, usuario.seller_rating, usuario.cars_sold, usuario.registration_date, usuario.last_login, usuario.is_active, usuario.is_admin))
                affected_rows = cursor.rowcount
                connection.commit()

            connection.close()
            return affected_rows
        except Exception as e:
            return Exception(e)

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
            return Exception(e)

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
            return Exception(e)
