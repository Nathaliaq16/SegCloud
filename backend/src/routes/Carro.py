from flask import Blueprint, request, jsonify
from models.CarroModel import CarroModel
from models.entities.Carro import Carro

carro_bp = Blueprint('carro_bp', __name__)


@carro_bp.route('/', methods=['GET'])
def get_carros():
    try:
        carros = CarroModel.get_carros()
        return jsonify(carros), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@carro_bp.route('/<id>', methods=['GET'])
def get_carro(id):
    try:
        carro = CarroModel.get_carro(id)
        if carro:
            return jsonify(carro), 200
        return jsonify({'message': 'Carro no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@carro_bp.route('/add', methods=['POST'])
def add_carro():
    try:
        data = request.json
        nuevo_carro = Carro(
            usuario_id=data['usuario_id'],
            location=data['location'],
            model=data['model'],
            price=data['price'],
            year=data['year'],
            km=data['km']
        )
        affected_rows = CarroModel.add_carro(nuevo_carro)
        if affected_rows == 1:
            return jsonify({'message': 'Carro agregado exitosamente'}), 201
        return jsonify({'message': 'Error al agregar el carro'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@carro_bp.route('/update/<id>', methods=['PUT'])
def update_carro(id):
    try:
        data = request.json
        carro_actualizado = Carro(
            id=id,
            usuario_id=data['usuario_id'],
            location=data['location'],
            model=data['model'],
            price=data['price'],
            year=data['year'],
            km=data['km']
        )
        affected_rows = CarroModel.update_carro(carro_actualizado)
        if affected_rows == 1:
            return jsonify({'message': 'Carro actualizado exitosamente'}), 200
        return jsonify({'message': 'Error al actualizar el carro'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@carro_bp.route('/delete/<id>', methods=['DELETE'])
def delete_carro(id):
    try:
        affected_rows = CarroModel.delete_carro(id)
        if affected_rows == 1:
            return jsonify({'message': 'Carro eliminado exitosamente'}), 200
        return jsonify({'message': 'Error al eliminar el carro'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500
