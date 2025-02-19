import jwt
import datetime
from decouple import config
from functools import wraps
from flask import request, jsonify

SECRET_KEY = config("SECRET_KEY", default="supersupersecreto")

def generate_jwt(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)  # Expira en 2 horas
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

def verify_jwt(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None  # Token expirado
    except jwt.InvalidTokenError:
        return None  # Token inválido

def require_jwt(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"error": "Token faltante"}), 401

        # Asegurar que el token tiene formato correcto
        token = token.replace("Bearer ", "").strip()

        payload = verify_jwt(token)
        if not payload:
            return jsonify({"error": "Token inválido o expirado"}), 401

        return f(*args, **kwargs)
    return decorated_function
