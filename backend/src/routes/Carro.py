from flask import Blueprint, request, jsonify
from utils.gcs_helper import upload_image_to_gcs
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
def add_carro(user_id):
    data = request.form
    file = request.files.get('imagen') 

    
    image_url = upload_image_to_gcs(file) if file else None

    nuevo_carro = Carro(
        usuario_id=user_id,
        location=data.get("location"),
        model=data.get("model"),
        price=float(data.get("price")),
        year=int(data.get("year")),
        km=int(data.get("km")),
        image_url=image_url
    )

    return jsonify(CarroModel.add_carro(nuevo_carro))

@carro_bp.route('/update/<int:id>', methods=['PUT'])
@require_jwt
def update_carro(id):
    data = request.form
    file = request.files.get('imagen')

    # Si hay una nueva imagen, subirla a GCS
    image_url = upload_image_to_gcs(file) if file else data.get('image_url')

    carro_actualizado = Carro(
        id=id,
        usuario_id=data.get("usuario_id"),
        location=data.get("location"),
        model=data.get("model"),
        price=float(data.get("price")),
        year=int(data.get("year")),
        km=int(data.get("km")),
        image_url=image_url
    )

    return jsonify(CarroModel.update_carro(carro_actualizado))

@carro_bp.route('/delete/<int:id>', methods=['DELETE'])
@require_jwt
def delete_carro(id):
    return jsonify(CarroModel.delete_carro(id))
