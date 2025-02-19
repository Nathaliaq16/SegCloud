import bcrypt

def hash_password(password):
    """
    Cifra una contraseña utilizando bcrypt.
    :param password: Contraseña en texto plano.
    :return: Contraseña cifrada (hash).
    """
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()

def check_password(password, hashed_password):
    """
    Verifica si una contraseña coincide con su hash.
    :param password: Contraseña en texto plano.
    :param hashed_password: Hash almacenado en la base de datos.
    :return: True si coinciden, False en caso contrario.
    """
    return bcrypt.checkpw(password.encode(), hashed_password.encode())