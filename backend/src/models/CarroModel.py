from database.db import get_connection, release_connection
from .entities.Carro import Carro
import bleach


class CarroModel:

    @classmethod
    def get_carros(cls):
        try:
            connection = get_connection()
            carros = []

            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM public.carros")
                resultset = cursor.fetchall()

                for carro in resultset:
                    car = Carro(
                        carro[0],
                        carro[1],
                        carro[2],
                        carro[3],
                        carro[4],
                        carro[5],
                        carro[6],
                    )
                    carros.append(car.to_JSON())
            return carros
        except Exception as e:
            print(f"Error en get_carros: {e}")
            return {"error": "Error al obtener los carros"}
        finally:
            release_connection(connection)

    @classmethod
    def get_carro(cls, id):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                if not isinstance(id, int) or id <= 0:
                    return {"error": "ID inválido"}

                cursor.execute(
                    "SELECT id, usuario_id, location, model, price, year, km FROM public.carros WHERE id=%s",
                    (id,),
                )
                carro = cursor.fetchone()

                if carro:
                    return Carro(*carro).to_JSON()  # Devolver el carro encontrado
                return {"message": "Carro no encontrado"}
        except Exception as e:
            print(f"Error en get_carro: {e}")
            return {"error": "Error al obtener el carro"}
        finally:
            release_connection(connection)

    @classmethod
    def add_carro(cls, carro):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                if not isinstance(carro.price, (int, float)) or carro.price <= 0:
                    return {"error": "El precio debe ser un número positivo"}
                if (
                    not isinstance(carro.year, int)
                    or carro.year < 1900
                    or carro.year > 2050
                ):
                    return {"error": "Año inválido"}
                
                # Sanitizar los campos de texto
                carro.model = bleach.clean(carro.model)
                carro.location = bleach.clean(carro.location)

                cursor.execute(
                    """INSERT INTO public.carros (usuario_id, location, model, price, year, km)
                                VALUES (%s, %s, %s, %s, %s, %s)""",
                    (
                        carro.usuario_id,
                        carro.location,
                        carro.model,
                        carro.price,
                        carro.year,
                        carro.km,
                    ),
                )

                affected_rows = cursor.rowcount
                connection.commit()

            connection.close()
            return affected_rows
        except Exception as e:
            print(f"Error en add_carro: {e}")
            return {"error": "Error al agregar el carro"}
        finally:
            release_connection(connection)

    @classmethod
    def delete_carro(cls, id):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute('DELETE FROM public."carros" WHERE id = %s', (id,))
                affected_rows = cursor.rowcount
                connection.commit()

            connection.close()
            return affected_rows
        except Exception as e:
            print(f"Error en delete_carro: {e}")
            return {"error": "Error al eliminar el carro"}
        finally:
            release_connection(connection)

    @classmethod
    def update_carro(cls, carro):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute(
                    """UPDATE public.carros SET usuario_id=%s, location=%s, model=%s, price=%s, year=%s, km=%s
                               WHERE id = %s""",
                    (
                        carro.usuario_id,
                        carro.location,
                        carro.model,
                        carro.price,
                        carro.year,
                        carro.km,
                        carro.id,
                    ),
                )
                affected_rows = cursor.rowcount
                connection.commit()

            connection.close()
            return affected_rows
        except Exception as e:
            print(f"Error en update_carro: {e}")
            return {"error": "Error al actualizar el carro"}
        finally:
            release_connection(connection)
