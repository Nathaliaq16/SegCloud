from flask import Blueprint, request, jsonify
from models.CarroModel import CarroModel
from models.entities.Carro import Carro
from utils.jwt_manager import require_jwt

carro_bp = Blueprint('carro_bp', __name__)

@carro_bp.route('/', methods=['GET'])
@require_jwt
def get_carros():
    return jsonify(CarroModel.get_carros())

@carro_bp.route('/<int:id>', methods=['GET'])
def get_carro(id):
    return jsonify(CarroModel.get_carro(id))

@carro_bp.route('/add', methods=['POST'])
@require_jwt
def add_carro():
    data = request.json
    nuevo_carro = Carro(**data)
    return jsonify(CarroModel.add_carro(nuevo_carro))

@carro_bp.route('/update/<int:id>', methods=['PUT'])
@require_jwt
def update_carro(id):
    data = request.json
    carro_actualizado = Carro(id=id, **data)
    return jsonify(CarroModel.update_carro(carro_actualizado))

@carro_bp.route('/delete/<int:id>', methods=['DELETE'])
@require_jwt
def delete_carro(id):
    return jsonify(CarroModel.delete_carro(id))
