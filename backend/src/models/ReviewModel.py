from database.db import get_connection, release_connection
from .entities.Review import Review
import bleach


class ReviewModel:

    @classmethod
    def get_reviews(cls):
        try:
            connection = get_connection()
            reviews = []

            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM public.review ORDER BY id ASC")
                resultset = cursor.fetchall()

                for review in resultset:
                    rev = Review(*review)
                    reviews.append(rev.to_JSON())

            connection.close()
            return reviews
        except Exception as e:
            print(f"Error en get_reviews: {e}")
            return {"error": "Error al obtener los reviews"}
        finally:
            release_connection(connection)

    @classmethod
    def get_review(cls, id):
        try:
            connection = get_connection()

            if not isinstance(id, int) or id <= 0:
                return {"error": "ID inválido"}
            
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT id, usuario_id, carro_id, rating, comment, review_date FROM public.review WHERE id=%s",
                    (id,),
                )
                review = cursor.fetchone()

                rev = None
                if review is not None:
                    rev = Review(*review).to_JSON()

            connection.close()
            return rev
        except Exception as e:
            print(f"Error en get_review: {e}")
            return {"error": "Error al obtener el review"}

    @classmethod
    def add_review(cls, review):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                if (
                    not isinstance(review.rating, (int, float))
                    or review.rating < 1
                    or review.rating > 5
                ):
                    return {"error": "El rating debe ser un número entre 1 y 5"}

                # Limpiar el comentario de HTML y JS
                review.comment = bleach.clean(review.comment)

                cursor.execute(
                    """INSERT INTO public.review (usuario_id, carro_id, rating, comment, review_date)
                                VALUES (%s, %s, %s, %s, %s)""",
                    (
                        review.usuario_id,
                        review.carro_id,
                        review.rating,
                        review.comment,
                        review.review_date,
                    ),
                )

                affected_rows = cursor.rowcount
                connection.commit()

            connection.close()
            return affected_rows
        except Exception as e:
            print(f"Error en add_review: {e}")
            return {"error": "Error al agregar el review"}
        finally:
            release_connection(connection)

    @classmethod
    def delete_review(cls, id):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM public.review WHERE id = %s", (id,))
                affected_rows = cursor.rowcount
                connection.commit()

            connection.close()
            return affected_rows
        except Exception as e:
            print(f"Error en delete_review: {e}")
            return {"error": "Error al eliminar el review"}

    @classmethod
    def update_review(cls, review):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute(
                    """UPDATE public.review SET usuario_id=%s, carro_id=%s, rating=%s, comment=%s, review_date=%s
                               WHERE id = %s""",
                    (
                        review.usuario_id,
                        review.carro_id,
                        review.rating,
                        review.comment,
                        review.review_date,
                        review.id,
                    ),
                )
                affected_rows = cursor.rowcount
                connection.commit()

            connection.close()
            return affected_rows
        except Exception as e:
            print(f"Error en update_review: {e}")
            return {"error": "Error al actualizar el review"}
