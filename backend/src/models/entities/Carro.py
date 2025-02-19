class Carro:

    def __init__(self, id=None, usuario_id=None, location=None, model=None, price=None, year=None, km=None):
        self.id = id
        self.usuario_id = usuario_id
        self.location = location
        self.model = model
        self.price = price
        self.year = year
        self.km = km

    def to_JSON(self):
        return {
            'id': self.id,
            'usuario_id': self.usuario_id,
            'location': self.location,
            'model': self.model,
            'price': self.price,
            'year': self.year,
            'km': self.km
        }
