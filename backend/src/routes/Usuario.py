from flask import Blueprint, request, jsonify
from models.UsuarioModel import UsuarioModel
from models.entities.Usuario import Usuario

usuario_bp = Blueprint('usuario_bp', __name__)


@usuario_bp.route('/', methods=['GET'])
def get_usuarios():
    try:
        usuarios = UsuarioModel.get_usuarios()
        return jsonify(usuarios), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@usuario_bp.route('/<id>', methods=['GET'])
def get_usuario(id):
    try:
        usuario = UsuarioModel.get_usuario(id)
        if usuario:
            return jsonify(usuario), 200
        return jsonify({'message': 'Usuario no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@usuario_bp.route('/add', methods=['POST'])
def add_usuario():
    try:
        data = request.json
        nuevo_usuario = Usuario(
            username=data['username'],
            email=data['email'],
            password_hash=data['password_hash'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            phone_number=data['phone_number'],
            address=data['address'],
            city=data['city'],
            country=data['country'],
            birthdate=data.get('birthdate'),
            is_seller=data.get('is_seller', False),
            seller_rating=data.get('seller_rating', 0.0),
            cars_sold=data.get('cars_sold', 0),
            registration_date=data.get('registration_date'),
            last_login=data.get('last_login'),
            is_active=data.get('is_active', True),
            is_admin=data.get('is_admin', False)
        )
        affected_rows = UsuarioModel.add_usuario(nuevo_usuario)
        if affected_rows == 1:
            return jsonify({'message': 'Usuario agregado exitosamente'}), 201
        return jsonify({'message': 'Error al agregar el usuario'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@usuario_bp.route('/update/<id>', methods=['PUT'])
def update_usuario(id):
    try:
        data = request.json
        usuario_actualizado = Usuario(
            id=id,
            username=data['username'],
            email=data['email'],
            password_hash=data['password_hash'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            phone_number=data['phone_number'],
            address=data['address'],
            city=data['city'],
            country=data['country'],
            birthdate=data.get('birthdate'),
            is_seller=data.get('is_seller', False),
            seller_rating=data.get('seller_rating', 0.0),
            cars_sold=data.get('cars_sold', 0),
            registration_date=data.get('registration_date'),
            last_login=data.get('last_login'),
            is_active=data.get('is_active', True),
            is_admin=data.get('is_admin', False)
        )
        affected_rows = UsuarioModel.update_usuario(usuario_actualizado)
        if affected_rows == 1:
            return jsonify({'message': 'Usuario actualizado exitosamente'}), 200
        return jsonify({'message': 'Error al actualizar el usuario'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@usuario_bp.route('/delete/<id>', methods=['DELETE'])
def delete_usuario(id):
    try:
        affected_rows = UsuarioModel.delete_usuario(id)
        if affected_rows == 1:
            return jsonify({'message': 'Usuario eliminado exitosamente'}), 200
        return jsonify({'message': 'Error al eliminar el usuario'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500
