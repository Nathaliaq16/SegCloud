from database.db import get_connection, release_connection
from .entities.Review import Review
import bleach

class ReviewModel:

    @classmethod
    def get_reviews(cls):
        """ Obtiene todas las reseñas de la base de datos. """
        try:
            connection = get_connection()
            reviews = []

            with connection.cursor() as cursor:
                cursor.execute("SELECT id, usuario_id, carro_id, rating, comment, review_date FROM public.review ORDER BY id ASC")
                resultset = cursor.fetchall()

                for review in resultset:
                    reviews.append(Review(*review).to_JSON())

            return reviews
        except Exception as e:
            print(f"Error en get_reviews: {e}")
            return {"error": "Error al obtener los reviews"}, 500
        finally:
            release_connection(connection)

    @classmethod
    def get_review(cls, id):
        """ Obtiene una reseña por su ID. """
        if not isinstance(id, int) or id <= 0:
            return {"error": "ID inválido"}, 400

        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute("SELECT id, usuario_id, carro_id, rating, comment, review_date FROM public.review WHERE id=%s", (id,))
                review = cursor.fetchone()

                if review:
                    return Review(*review).to_JSON(), 200
                return {"message": "Review no encontrado"}, 404
        except Exception as e:
            print(f"Error en get_review: {e}")
            return {"error": "Error al obtener el review"}, 500
        finally:
            release_connection(connection)

    @classmethod
    def add_review(cls, review):
        """ Agrega una nueva reseña a la base de datos. """
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                if not isinstance(review.rating, (int, float)) or review.rating < 1 or review.rating > 5:
                    return {"error": "El rating debe ser un número entre 1 y 5"}, 400

                # Limpiar el comentario de HTML y JS
                review.comment = bleach.clean(review.comment)

                cursor.execute("""
                    INSERT INTO public.review (usuario_id, carro_id, rating, comment, review_date)
                    VALUES (%s, %s, %s, %s, %s)
                """, (review.usuario_id, review.carro_id, review.rating, review.comment, review.review_date))

                if cursor.rowcount == 1:
                    connection.commit()
                    return {"message": "Review agregado exitosamente"}, 201
                return {"error": "No se pudo agregar el review"}, 500
        except Exception as e:
            print(f"Error en add_review: {e}")
            return {"error": f"Error interno: {str(e)}"}, 500
        finally:
            release_connection(connection)

    @classmethod
    def delete_review(cls, id):
        """ Elimina una reseña por su ID. """
        if not isinstance(id, int) or id <= 0:
            return {"error": "ID inválido"}, 400

        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM public.review WHERE id = %s", (id,))
                
                if cursor.rowcount == 1:
                    connection.commit()
                    return {"message": "Review eliminado exitosamente"}, 200
                return {"error": "Review no encontrado"}, 404
        except Exception as e:
            print(f"Error en delete_review: {e}")
            return {"error": f"Error interno: {str(e)}"}, 500
        finally:
            release_connection(connection)

    @classmethod
    def update_review(cls, review):
        """ Actualiza los datos de una reseña en la base de datos. """
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE public.review 
                    SET usuario_id=%s, carro_id=%s, rating=%s, comment=%s, review_date=%s
                    WHERE id = %s
                """, (review.usuario_id, review.carro_id, review.rating, review.comment, review.review_date, review.id))

                if cursor.rowcount == 1:
                    connection.commit()
                    return {"message": "Review actualizado exitosamente"}, 200
                return {"error": "Review no encontrado"}, 404
        except Exception as e:
            print(f"Error en update_review: {e}")
            return {"error": f"Error interno: {str(e)}"}, 500
        finally:
            release_connection(connection)
