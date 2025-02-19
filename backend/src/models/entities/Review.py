class Review:

    def __init__(self, id=None, usuario_id=None, carro_id=None, rating=None, comment=None, review_date=None):
        self.id = id
        self.usuario_id = usuario_id
        self.carro_id = carro_id
        self.rating = rating
        self.comment = comment
        self.review_date = review_date

    def to_JSON(self):
        return {
            'id': self.id,
            'usuario_id': self.usuario_id,
            'carro_id': self.carro_id,
            'rating': self.rating,
            'comment': self.comment,
            'review_date': str(self.review_date) if self.review_date else None
        }