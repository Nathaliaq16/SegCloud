class Usuario:

    def __init__(self, id=None, username=None, email=None, password_hash=None, first_name=None, last_name=None, phone_number=None, address=None, city=None, country=None, birthdate=None, is_seller=False, seller_rating=0.0, cars_sold=0, registration_date=None, last_login=None, is_active=True, is_admin=False):
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.address = address
        self.city = city
        self.country = country
        self.birthdate = birthdate
        self.is_seller = is_seller
        self.seller_rating = seller_rating
        self.cars_sold = cars_sold
        self.registration_date = registration_date
        self.last_login = last_login
        self.is_active = is_active
        self.is_admin = is_admin

    def to_JSON(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'password_hash': self.password_hash,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone_number': self.phone_number,
            'address': self.address,
            'city': self.city,
            'country': self.country,
            'birthdate': str(self.birthdate) if self.birthdate else None,
            'is_seller': self.is_seller,
            'seller_rating': float(self.seller_rating),
            'cars_sold': self.cars_sold,
            'registration_date': str(self.registration_date) if self.registration_date else None,
            'last_login': str(self.last_login) if self.last_login else None,
            'is_active': self.is_active,
            'is_admin': self.is_admin
        }
