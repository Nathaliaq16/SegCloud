from flask import Blueprint, request, jsonify
from models.UsuarioModel import UsuarioModel
from models.entities.Usuario import Usuario
from utils.jwt_manager import generate_jwt, require_jwt
from utils.security import check_password
from app import limiter

usuario_bp = Blueprint('usuario_bp', __name__)

@usuario_bp.route('/login', methods=['POST'])
@limiter.limit("3 per minute")
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    usuario, status_code = UsuarioModel.get_usuario_by_email(email)
    if "error" in usuario or not usuario:
        return jsonify(usuario), status_code

    if not check_password(password, usuario["password_hash"]):
        return jsonify({"error": "Contraseña incorrecta"}), 401

    token = generate_jwt(usuario["id"])
    return jsonify({"token": token}), 200

@usuario_bp.route('/<int:id>', methods=['GET'])
@require_jwt
def get_usuario(id):
    return jsonify(UsuarioModel.get_usuario(id))

@usuario_bp.route('/add', methods=['POST'])
def add_usuario():
    data = request.json
    nuevo_usuario = Usuario(**data)
    return jsonify(UsuarioModel.add_usuario(nuevo_usuario))

@usuario_bp.route('/delete/<int:id>', methods=['DELETE'])
@require_jwt
def delete_usuario(id):
    return jsonify(UsuarioModel.delete_usuario(id))
