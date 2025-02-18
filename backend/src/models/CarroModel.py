from database.db import get_connection
from .entities.Carro import Carro


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
                    car = Carro(carro[0], carro[1], carro[2], carro[3], carro[4], carro[5], carro[6])
                    carros.append(car.to_JSON())

            connection.close()
            return carros
        except Exception as e:
            return Exception(e)

    @classmethod
    def get_carro(cls, id):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM public.carros WHERE id=%s", (id,))
                carro = cursor.fetchone()

                car = None
                if carro is not None:
                    car = Carro(carro[0], carro[1], carro[2], carro[3], carro[4], carro[5], carro[6])
                    car = car.to_JSON()

            connection.close()
            return car
        except Exception as e:
            return Exception(e)

    @classmethod
    def add_carro(cls, carro):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute("""INSERT INTO public.carros (usuario_id, location, model, price, year, km)
                               VALUES (%s, %s, %s, %s, %s, %s)""",
                               (carro.usuario_id, carro.location, carro.model, carro.price, carro.year, carro.km))
                affected_rows = cursor.rowcount
                connection.commit()

            connection.close()
            return affected_rows
        except Exception as e:
            return Exception(e)

    @classmethod
    def delete_carro(cls, id):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM public.\"carros\" WHERE id = %s", (id,))
                affected_rows = cursor.rowcount
                connection.commit()

            connection.close()
            return affected_rows
        except Exception as e:
            return Exception(e)

    @classmethod
    def update_carro(cls, carro):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute("""UPDATE public.carros SET usuario_id=%s, location=%s, model=%s, price=%s, year=%s, km=%s
                               WHERE id = %s""",
                               (carro.usuario_id, carro.location, carro.model, carro.price, carro.year, carro.km, carro.id))
                affected_rows = cursor.rowcount
                connection.commit()

            connection.close()
            return affected_rows
        except Exception as e:
            return Exception(e)
