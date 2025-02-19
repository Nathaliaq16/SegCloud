from database.db import get_connection, release_connection
from .entities.Carro import Carro
import bleach

class CarroModel:

    @classmethod
    def get_carros(cls):
        """ Obtiene todos los carros de la base de datos. """
        try:
            connection = get_connection()
            carros = []

            with connection.cursor() as cursor:
                cursor.execute("SELECT id, usuario_id, location, model, price, year, km FROM public.carros")
                resultset = cursor.fetchall()

                for carro in resultset:
                    carros.append(Carro(*carro).to_JSON())

            return carros
        except Exception as e:
            print(f"Error en get_carros: {e}")
            return {"error": "Error al obtener los carros"}, 500
        finally:
            release_connection(connection)

    @classmethod
    def get_carro(cls, id):
        """ Obtiene un carro por su ID. """
        if not isinstance(id, int) or id <= 0:
            return {"error": "ID inválido"}, 400

        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute("SELECT id, usuario_id, location, model, price, year, km FROM public.carros WHERE id=%s", (id,))
                carro = cursor.fetchone()

                if carro:
                    return Carro(*carro).to_JSON(), 200
                return {"message": "Carro no encontrado"}, 404
        except Exception as e:
            print(f"Error en get_carro: {e}")
            return {"error": "Error al obtener el carro"}, 500
        finally:
            release_connection(connection)

    @classmethod
    def add_carro(cls, carro):
        """ Agrega un nuevo carro a la base de datos. """
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                if not isinstance(carro.price, (int, float)) or carro.price <= 0:
                    return {"error": "El precio debe ser un número positivo"}, 400
                if not isinstance(carro.year, int) or carro.year < 1900 or carro.year > 2050:
                    return {"error": "Año inválido"}, 400

                # Sanitizar los campos de texto
                carro.model = bleach.clean(carro.model)
                carro.location = bleach.clean(carro.location)

                cursor.execute("""
                    INSERT INTO public.carros (usuario_id, location, model, price, year, km)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (carro.usuario_id, carro.location, carro.model, carro.price, carro.year, carro.km))

                if cursor.rowcount == 1:
                    connection.commit()
                    return {"message": "Carro agregado exitosamente"}, 201
                return {"error": "No se pudo agregar el carro"}, 500
        except Exception as e:
            print(f"Error en add_carro: {e}")
            return {"error": f"Error interno: {str(e)}"}, 500
        finally:
            release_connection(connection)

    @classmethod
    def delete_carro(cls, id):
        """ Elimina un carro de la base de datos por su ID. """
        if not isinstance(id, int) or id <= 0:
            return {"error": "ID inválido"}, 400

        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute('DELETE FROM public.carros WHERE id = %s', (id,))
                
                if cursor.rowcount == 1:
                    connection.commit()
                    return {"message": "Carro eliminado exitosamente"}, 200
                return {"error": "Carro no encontrado"}, 404
        except Exception as e:
            print(f"Error en delete_carro: {e}")
            return {"error": f"Error interno: {str(e)}"}, 500
        finally:
            release_connection(connection)

    @classmethod
    def update_carro(cls, carro):
        """ Actualiza los datos de un carro en la base de datos. """
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE public.carros 
                    SET usuario_id=%s, location=%s, model=%s, price=%s, year=%s, km=%s
                    WHERE id = %s
                """, (carro.usuario_id, carro.location, carro.model, carro.price, carro.year, carro.km, carro.id))

                if cursor.rowcount == 1:
                    connection.commit()
                    return {"message": "Carro actualizado exitosamente"}, 200
                return {"error": "Carro no encontrado"}, 404
        except Exception as e:
            print(f"Error en update_carro: {e}")
            return {"error": f"Error interno: {str(e)}"}, 500
        finally:
            release_connection(connection)
